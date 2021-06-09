from django import forms
from django.forms import formset_factory

class tijdschrijfUnit(forms.Form):
    persoonID = forms.IntegerField(widget=forms.HiddenInput)
    projectactiviteitID = forms.IntegerField(widget=forms.HiddenInput)
    datum = forms.DateField(widget=forms.HiddenInput)
    uren = forms.DecimalField(decimal_places=2,max_digits=4,max_value=24)

tijdschrijfSet = formset_factory(tijdschrijfUnit, extra=0)