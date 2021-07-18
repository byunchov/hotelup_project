from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import FloatField


class Room(models.Model):
    ROOM_CATEGORIES = (
        ('STD', 'Стандарт'),
        ('BSN', 'Бизнес'),
        ('LUX', 'Лукс'),
        ('ELUX', 'Ултра-лукс'),
        ('FAM', 'Фемили'),
    )

    number = models.IntegerField()
    beds = models.IntegerField()
    capacity = models.IntegerField()
    rate = models.FloatField()
    category = models.CharField(max_length=12, choices=ROOM_CATEGORIES)
    description = models.TextField(null=True)
    thumbnail = models.ImageField(upload_to="room_thumbnails", height_field=None, width_field=None, default='0.jpeg')

    def __str__(self) -> str:
        categories = dict(self.ROOM_CATEGORIES)
        return f'{self.number}. {categories.get(self.category)} - ({self.capacity}, {self.beds})'


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
