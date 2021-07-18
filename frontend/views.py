from django.contrib import messages
from django.http.response import JsonResponse
from frontend.filters import RoomFilter
from frontend.utilities.booking_helper import is_room_available
from frontend.models import Booking, Room
from django.shortcuts import redirect, render
from .forms import DatePickerForm
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

# Create your views here.
def home_view(request):
    return render(request, 'frontend/home.html', {})

def get_avail_rooms(request):
    context = dict()    

    # form = CheckRoomAvailableForm(request.POST or None)

    # if request.method == "POST":
    #     category = request.POST.get('room_category', None)
    #     room_list = Room.objects.filter(category=category)
    #     avail_list = []

    #     if form.is_valid():
    #         data = form.cleaned_data

    #     for room in room_list:
    #         if is_room_available(room, data['check_in'], data['check_out']):
    #             avail_list.append(room)
        
    #     context['avail_list'] = avail_list

    # context['form'] = form

    avail_list = []
    date_form = DatePickerForm(request.GET or None)
    filt = RoomFilter(request.GET, queryset=Room.objects.all())

    # checkin = request.GET.get('checkin', datetime.date.today())
    # checkout = request.GET.get('checkout', datetime.date.today() + datetime.timedelta(days=1))

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

    # print(request.session['start_date'])
    # print(request.session['end_date'])
    # print(request.session['num_guests'])
    # print(request.session['nights'])

    return render(request, 'frontend/list.html', context)

@login_required
def user_dash(request):
    # print(request.session['end_date'])

    context = dict()
    booking_list = Booking.objects.filter(user=request.user)

    aggr = Booking.objects.values('status').annotate(dcount=Count('status')).order_by()
    
    counts = {}

    for c in aggr:
        counts[c['status']] = c['dcount']

    context['booking_list'] = booking_list
    context['counts'] = counts

    return render(request, 'frontend/dash.html', context)

@login_required
def book_room(request, pk):
    context = {}
    billing = {}
    room = Room.objects.get(pk=pk)

    checkin = request.session.get('start_date', None)
    checkout = request.session.get('end_date', None)
    num_guests = int(request.session.get('num_guests', 1) or 1)
    nights = int(request.session.get('nights', 1) or 1)

    billing['room_stay'] = round(room.rate * num_guests * nights, 2)
    billing['tax'] = round(billing['room_stay'] * 0.02, 2)
    billing['amount'] = round(billing['room_stay'] + billing['tax'], 2)

    request.session['total_amount'] = billing['amount'] 

    context['room'] = room
    context['billing'] = billing
    context['checkin'] = checkin
    context['checkout'] = checkout
    context['num_guests'] = num_guests
    context['nights'] = nights
    
    return render(request, 'frontend/book.html', context)

@login_required
def confirm_booking(request, pk):
    checkin = request.session.get('start_date', None)
    checkout = request.session.get('end_date', None)
    amount = request.session.get('total_amount', 0) 

    if checkin and checkout:
        room = Room.objects.get(pk=pk)
        start_date = datetime.datetime.strptime(checkin, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(checkout, '%Y-%m-%d').date()

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
        messages.error(request, 'Невалидни параметри в заявката за резервация!')
        return redirect('book_room', pk=pk)

@require_POST
def cancel_booking(request):
    id = request.POST['booking_id']
    print(f"Booking with ID {id} was cancelled")
    if id:
        booking: Booking = Booking.objects.get(pk=id)
        if booking:
            booking.status = Booking.BOOKING_STATUS[2][0] # canceled
            booking.save()

            print(booking)

            return JsonResponse({'status': 200, 'msg': 'Booking cancelled successfully.'})
        else:
            return JsonResponse({'status': 404, 'msg': f'Booking {id} was not found!'})
    
    return JsonResponse({'status': 401, 'msg': 'ID was not provided!'})
