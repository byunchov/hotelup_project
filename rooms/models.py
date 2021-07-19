from django.db import models


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
    thumbnail = models.ImageField(upload_to="room_thumbnails", height_field=None, width_field=None, default='room_thumbnails/t101.jpg')

    def __str__(self) -> str:
        categories = dict(self.ROOM_CATEGORIES)
        return f'{self.number}. {categories.get(self.category)} - ({self.capacity}, {self.beds})'
