from django import forms

class tijdschrijfForm(forms.Form):
    testvak = forms.CharField(label='testvak', max_length=100)