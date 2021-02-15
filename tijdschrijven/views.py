from django.shortcuts import render
from tijdschrijven.models import Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class ProjectCreate(CreateView):
    model = Project
    fields=['Titel', 'ProjectTemplateID', 'Omschrijving', 'ParentID', 'AanmakerID', 'GeldigVan', 'GeldigTot', 'Actief']
    #initial = {'date_of_death': '11/06/2020'}

class ProjectUpdate(UpdateView):
    model = Project
    fields=['Titel', 'ProjectTemplateID', 'Omschrijving', 'ParentID', 'AanmakerID', 'GeldigVan', 'GeldigTot', 'Actief']

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projecten')