from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room


class Booking(models.Model):

    BOOKING_STATUS = (
        ('active', 'Активна'),
        ('finished', 'Завършена'),
        ('canceled', 'Отменена'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(choices=BOOKING_STATUS, max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()

    def __str__(self) -> str:
        return f'Резервация #{self.pk} на стая {self.room.number} за периода от {self.check_in} до {self.check_out} [{self.status}]'
