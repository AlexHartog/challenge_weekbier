from django import forms

from .models import Player, Checkin


class CheckinForm(forms.ModelForm):
    class Meta:
        model = Checkin
        fields = ['player', 'date', 'place', 'city']
        labels = {'text': ''}
