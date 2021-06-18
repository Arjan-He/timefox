from django import forms


class frmGridCell(forms.Form):
    project_activiteit = forms.NumberInput()
    datum = forms.DateTimeField()
    tijdsduur = forms.DecimalField(min_value=0, max_value=24, max_digits=4, decimal_places=2)