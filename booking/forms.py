from django import forms


class DatePickerForm(forms.Form):
    checkin = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}), label='Дата на настаняване')
    checkout = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}), label='Дата на напускане')