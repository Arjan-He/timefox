from django.shortcuts import render
from tijdschrijven.models import Project, Persoon, Abonnement, GeschrevenTijd
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# from .forms import tijdschrijfForm
from utils import dateFunctions
import datetime
from datetime import date
from utils import verwerkUren
from django.db.models import Q
# Create your views here.

def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')

@login_required
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
    tijdgridOud = GeschrevenTijd.tijdoverzicht(eerstedagweek,1)
    tijdgrid = []

    for i in range(7):
        deDatum = eerstedagweek + datetime.timedelta(days=i)
        therecord = Abonnement.objects.filter(ProjectID__GeldigVan__lte = eerstedagweek,
                                              ProjectID__GeldigTot__gte = eerstedagweek,
                                              PersoonID__id = 3)\
                    .filter(Q(geschreventijd__Datum=deDatum) | Q(geschreventijd__Datum__isnull=True))\
                    .values('id','PersoonID','ProjectID','ProjectID__Titel'
                            ,'ProjectID__GeldigVan','ProjectID__GeldigTot'
                            ,'geschreventijd__TijdsDuur')

        tijdgrid.append(therecord)

    dagenInWeek = dateFunctions.daysInWeek(2)

    context = {'dagenindeweek':dagenInWeek,
               'tijdgrid':tijdgridOud,
               'datum': datum.isoformat()[0:10],
               'newgrid' : tijdgrid}

    return render(request,'urenschrijven.html',context=context)

