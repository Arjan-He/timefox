from django.shortcuts import render
from tijdschrijven.models import Project, Persoon, Abonnement, GeschrevenTijd
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from utils import dateFunctions
import datetime
from datetime import date
from utils import verwerkUren
from utils import projectFuncties

# Create your views here.

def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')

@login_required
def projecten(request):
    projecten = Project.objects.all()

    parents = projectFuncties.geefProjectParents(15)
    children = projectFuncties.geefProjectChildren(15)

    context = {'projecten': projecten,
               'children': children,
               'parents': parents,}
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

@login_required
def abonnementen(request):
    abonnementen = Abonnement.objects.all()
    context = {'abonnementen': abonnementen,}
    return render(request,'abonnement.html', context=context)


class AbonnementCreate(CreateView):
    model = Abonnement
    fields=['PersoonID', 'ProjectID','OriginalObjectID']
    success_url = reverse_lazy('abonnementen')

@login_required
def urenschrijven(request):

    # Dit moet een veld worden in Persoon (laatst bezochte week)
    datum = date.today()
    
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
    tijdgrid = GeschrevenTijd.tijdoverzicht(eerstedagweek, request.user.id)

    # argument=2: de eerste twee letters van de dagen
    dagenInWeek = dateFunctions.daysInWeek(2)

    context = {'dagenindeweek':dagenInWeek,
               'tijdgrid':tijdgrid,
               'datum': datum.isoformat()[0:10],}

    return render(request,'urenschrijven.html',context=context)
