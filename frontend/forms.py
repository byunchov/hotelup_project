from frontend.models import Room
from django import forms

class CheckRoomAvailableForm(forms.Form):
    check_in = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}))
    room_category = forms.ChoiceField(choices=Room.ROOM_CATEGORIES)


class DatePickerForm(forms.Form):
    checkin = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}), label='Дата на настаняване')
    checkout = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}), label='Дата на напускане')