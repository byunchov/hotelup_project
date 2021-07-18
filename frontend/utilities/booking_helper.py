import datetime
from frontend.models import Booking, Room


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

'''
from frontend.utilities.booking_helper import is_room_available
from frontend.models import Room, Booking
r104 = Room.objects.filter(number=104).first()
is_room_available(r104, '2021-07-12','2021-07-21')
'''

# def test_functions():
#     checkin = '2021-07-21'
#     checkout = '2021-07-25'
#     avail_rooms = []

#     lux_rooms = Room.objects.filter(category='LUX', capacity=2)

# for room in lux_rooms:
#     if is_room_available(room, checkin, checkout):
#         avail_rooms.append(room)

# print(avail_rooms)
