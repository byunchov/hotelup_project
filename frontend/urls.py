from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('list_rooms/', views.get_avail_rooms, name='list_rooms'),
    path('dashboard/', views.user_dash, name='user_dash'),
    path('cancel_booking/', views.cancel_booking, name='cancel_booking'),
    path('book_room/<int:pk>', views.book_room, name='book_room'),
    path('confirm_booking/<int:pk>', views.confirm_booking, name='confirm_booking'),
]