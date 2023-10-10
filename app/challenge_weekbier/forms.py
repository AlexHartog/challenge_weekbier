from datetime import date

from django import forms

from .models import Checkin, Player


class CheckinForm(forms.ModelForm):
    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        label="Naam",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Checkin

        fields = ["player", "date", "place", "city"]

        labels = {
            "player": "Naam",
            "date": "Datum",
            "place": "Etablissement",
            "city": "Plaats",
        }
        widgets = {
            "date": forms.widgets.DateInput(attrs={"type": "date"}, format="%d/%m/%Y"),
            "place": forms.widgets.TextInput(attrs={"class": "form-input"}),
            "city": forms.widgets.TextInput(attrs={"class": "form-input"}),
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="CSV bestand")
