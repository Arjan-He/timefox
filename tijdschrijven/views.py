from django.shortcuts import render
from tijdschrijven.models import Project, Persoon, Abonnement, GeschrevenTijd
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import tijdschrijfForm
from utils import dateFunctions
from datetime import date
# Create your views here.

def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')


def projecten(request):
   projecten = Project.objects.all()
   context = {'projecten': projecten,}
   # Render the HTML template index.html with the data in the context variable
   return render(request, 'projecten.html', context=context)


class ProjectCreate(CreateView):
    model = Project
    fields=['Titel', 'ProjectTemplateID', 'Omschrijving', 'ParentID', 'AanmakerID', 'GeldigVan', 'GeldigTot', 'Actief']
    success_url = reverse_lazy('projecten')


class ProjectUpdate(UpdateView):
    model = Project
    fields=['Titel', 'ProjectTemplateID', 'Omschrijving', 'ParentID', 'AanmakerID', 'GeldigVan', 'GeldigTot', 'Actief']
    success_url = reverse_lazy('projecten')


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projecten')


def abonnementen(request):
    abonnementen = Abonnement.objects.all()
    context = {'abonnementen': abonnementen,}
    return render(request,'abonnement.html', context=context)


class AbonnementCreate(CreateView):
    model = Abonnement
    fields=['PersoonID', 'ProjectID','OriginalObjectID']
    success_url = reverse_lazy('abonnementen')


def urenschrijven(request):

    datum = date.today()

    eerstedagweek = dateFunctions.fdow(datum)
    laatstedagweek = dateFunctions.ldow(datum)

    abonnementen = Abonnement.objects.filter(ProjectID__GeldigVan__lte = eerstedagweek
                                            ,ProjectID__GeldigTot__gte = laatstedagweek
                                            ,ProjectID__Actief = True)

    datumsinweek = GeschrevenTijd.datumsinweek(eerstedagweek)
    tijdgrid = GeschrevenTijd.tijdoverzicht(eerstedagweek,1)
    dagenInWeek = dateFunctions.dagenInWeek(2)

    if request.method == 'POST':
    
        form = tijdschrijfForm(request.POST)

        #if form.is_valid():

    context = {'abonnementen': abonnementen,
               'dagenindeweek':dagenInWeek,
               'datumsinweek': datumsinweek,
               'eerstedag': eerstedagweek.strftime("%Y-%m-%d"),
               'tijdgrid':tijdgrid,}

    # dageninweek 
  
    return render(request,'urenschrijven.html',context=context)

