from django import forms


class tijdschrijfUnit(forms.Form):
    abonnement = forms.IntegerField(widget=forms.HiddenInput)
    datum = forms.DateField(widget=forms.HiddenInput)
    uren = forms.DecimalField(decimal_places=2, max_digits=4, max_value=24)
