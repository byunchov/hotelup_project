from django.db.models import fields
import django_filters
from .models import Room

class RoomFilter(django_filters.FilterSet):
    # checkin_date = django_filters.DateFilter(field_name='checkin')
    # checkout_date = django_filters.DateFilter(field_name='checkout')

    ORDERBY_PRICE_CHOICES = (
        ('asc', 'От ниска към висока'),
        ('desc', 'От висока към ниска'),
    )

    model = Room

    category = django_filters.ChoiceFilter(field_name='category', label='Категория', choices=Room.ROOM_CATEGORIES)
    capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte', label='Брой гости')
    beds = django_filters.NumberFilter(field_name='beds', lookup_expr='gte', label='Брой легла')
    orderby_price = django_filters.ChoiceFilter(label='Подреди по цена', choices=ORDERBY_PRICE_CHOICES, method='order_by_price')

    def order_by_price(self, queryset, name, value):
        expression = 'rate' if value == 'asc' else '-rate'
        return queryset.order_by(expression)

    # class Meta:
    #     model = Room
    #     fields = ('category',)
        # fields = ('beds','capacity','category',)
        # fields = {
        #     'capacity':('exact', 'gte'),
        #     'beds':('exact', 'gte'),
        #     'category':('exact',),            
        # }

