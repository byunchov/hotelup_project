from booking.models import Booking
from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required

@login_required
def user_dash(request):

    context = dict()
    booking_list = Booking.objects.filter(user=request.user)

    aggr = Booking.objects.values('status').annotate(dcount=Count('status')).order_by()
    
    counts = {}

    for c in aggr:
        counts[c['status']] = c['dcount']

    context['booking_list'] = booking_list
    context['counts'] = counts

    return render(request, 'dashboard/dash.html', context)
