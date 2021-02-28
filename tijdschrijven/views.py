from django.shortcuts import render
from tijdschrijven.models import Project, Persoon, Abonnement, GeschrevenTijd
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# from .forms import tijdschrijfForm
from utils import dateFunctions
from datetime import date
from utils import verwerkUren
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
    weeknummer = []

    if request.method == 'POST':
        # form = tijdschrijfForm(request.POST)
        # if form.is_valid():
        verwerkUren.walkTheGrid(request.POST)

        if request.POST['weeknummer']:
            weeknummer = request.POST['weeknummer'].split('week:')
            weeknummer = [x.strip() for x in weeknummer] 
            datum, datum2 = dateFunctions.getDateRangeFromWeek(weeknummer[0],weeknummer[1])


    eerstedagweek = dateFunctions.fdow(datum)
    laatstedagweek = dateFunctions.ldow(datum)


    datumsinweek = GeschrevenTijd.datumsinweek(eerstedagweek)
    tijdgrid = GeschrevenTijd.tijdoverzicht(eerstedagweek,1)
    dagenInWeek = dateFunctions.daysInWeek(2)
    velden = []



    context = {'dagenindeweek':dagenInWeek,
               'tijdgrid':tijdgrid,}

    # dageninweek 
  
    return render(request,'urenschrijven.html',context=context)

