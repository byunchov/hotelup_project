import datetime
from booking.models import Booking


def is_room_available(room, checkin_date, checkout_date):

    if type(checkin_date) == str:
        checkin_date = datetime.datetime.strptime(checkin_date, '%Y-%m-%d').date()

    if type(checkout_date) == str:
        checkout_date = datetime.datetime.strptime(checkout_date, '%Y-%m-%d').date()

    available_rooms = []
    bookings_list = Booking.objects.filter(room=room, status='active')

    for booking in bookings_list:
        expr: bool = (booking.check_in > checkout_date or booking.check_out < checkin_date)
        available_rooms.append(expr)

    return all(available_rooms)

