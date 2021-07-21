from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from .filters import RoomFilter
from .utilities.booking_helper import is_room_available
from .models import Booking
from rooms.models import Room
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import DatePickerForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import urllib


def get_avail_rooms(request):
    context = dict()

    avail_list = []
    date_form = DatePickerForm(request.GET or None)
    filt = RoomFilter(request.GET, queryset=Room.objects.all())

    checkin = request.GET.get('checkin', None)
    checkout = request.GET.get('checkout', None)
    page = request.GET.get('page', 1)

    if checkin and checkout:
        for room in filt.qs:
            if is_room_available(room, checkin, checkout):
                avail_list.append(room)
        
        start_date = datetime.datetime.strptime(checkin, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(checkout, '%Y-%m-%d').date()
        nights = (end_date-start_date).days
        request.session['nights'] = nights

    paginator = Paginator(avail_list, 5)

    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    context['filter'] = filt
    context['avail_list'] = rooms
    context['date_form'] = date_form    

    request.session['start_date'] = checkin
    request.session['end_date'] = checkout
    request.session['num_guests'] = request.GET.get('capacity', 1)
    
    return render(request, 'booking/list.html', context)


@login_required
def book_room(request, pk):
    context = {}
    billing = {}
    room = Room.objects.get(pk=pk)

    checkin = request.session.get('start_date', None)
    checkout = request.session.get('end_date', None)
    num_guests = int(request.session.get('num_guests', 1) or 1)
    nights = int(request.session.get('nights', 1) or 1)

    if checkin and checkout:
        billing['room_stay'] = round(room.price * num_guests * nights, 2)
        billing['tax'] = round(billing['room_stay'] * 0.02, 2)
        billing['amount'] = round(billing['room_stay'] + billing['tax'], 2)

        request.session['total_amount'] = billing['amount'] 

        context['room'] = room
        context['billing'] = billing
        context['checkin'] = checkin
        context['checkout'] = checkout
        context['num_guests'] = num_guests
        context['nights'] = nights
        
        return render(request, 'booking/book.html', context)
    else:
        return redirect('list_rooms')

@login_required
def confirm_booking(request, pk):
    checkin = request.session.get('start_date', None)
    checkout = request.session.get('end_date', None)
    amount = request.session.get('total_amount', 0) 
    num_guests = int(request.session.get('num_guests', 1) or 1)

    if checkin and checkout:
        room: Room = Room.objects.get(pk=pk)
        start_date = datetime.datetime.strptime(checkin, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(checkout, '%Y-%m-%d').date()

        if is_room_available(room, start_date, end_date):
            booking = Booking(room=room, user=request.user, check_in=start_date, check_out=end_date, status='active', total_price=amount)
            booking.save()

            del request.session['nights']
            del request.session['start_date']
            del request.session['end_date']
            del request.session['num_guests']
            del request.session['total_amount']

            messages.success(request, f'Резервация #{booking.pk} е напрваена успешно!')
            
            return redirect('user_dash')
        else:
            redirect_params = { 'checkin': checkin, 'checkout': checkout, 'capacity': num_guests}
            url = reverse('list_rooms')
            url_params = urllib.parse.urlencode(redirect_params)

            messages.error(request, f'Стая #{room.number} е заета за избрания от вас период! Моля, изберете друга!')

            return HttpResponseRedirect(f"{url}?{url_params}")
    else:
        return redirect('list_rooms')

@require_POST
def cancel_booking(request):
    id = request.POST['booking_id']
    if id:
        booking: Booking = Booking.objects.get(pk=id)
        if booking:
            booking.status = Booking.BOOKING_STATUS[2][0] # canceled
            booking.save()

            print(booking)

            return JsonResponse({'status': 200, 'msg': f'Резервация #{id} беше отменена успешно.'})
        else:
            return JsonResponse({'status': 404, 'msg': f'Резервация #{id} не беше открита!'})
    
    return JsonResponse({'status': 401, 'msg': 'Параметър [ID] не е предоставен!'})
