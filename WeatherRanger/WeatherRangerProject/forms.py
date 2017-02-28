from django import forms
from django.contrib.auth.models import User
from WeatherRangerProject.models import TemperatureRange

class TemperatureRangeForm(forms.ModelForm):
    class Meta:
        model = TemperatureRange
        exclude =  ('user', 'is_in_five_day_range', 'is_in_range', 'is_in_sixteen_day_range')

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password', 'email', 'username')