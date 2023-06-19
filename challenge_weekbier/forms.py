from django import forms
from datetime import date


from .models import Player, Checkin


class CheckinForm(forms.ModelForm):
    #TODO: Can we use a ModelChoiceField for player?
    #TODO: Can we get the data formatted correctly?

    # date = forms.DateField(
    #     input_formats=["%d/%m/%Y"],
    #     widget=forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y'),
    #     initial=date.today()
    # )

    class Meta:
        model = Checkin
        fields = ['player', 'date', 'place', 'city']
        labels = {'text': ''}
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}, format="%d/%m/%Y"),
        }
