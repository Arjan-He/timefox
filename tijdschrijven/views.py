from django.shortcuts import render
from tijdschrijven.models import Project, Abonnement, GeschrevenTijd
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from utils import dateFunctions
# import datetime
from datetime import date
from utils import verwerkUren
from utils import projectFuncties
from django.db.models import Sum


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html')


@login_required
def projecten(request):
    projecten = Abonnement.objects.filter(persoon=request.user.id).values('id','project__titel','project__omschrijving','project__geldigvan','project__geldigtot')
    projecten_dict = {'projecten': projecten}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'projecten.html',context = projecten_dict )


class ProjectCreate(CreateView):
    model = Project
    fields = ['titel',
              'ProjectTemplateID',
              'Omschrijving',
              'ParentID',
              'AanmakerID',
              'GeldigVan',
              'GeldigTot',
              'Actief']
    success_url = reverse_lazy('projecten')


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['titel', 'ProjectTemplateID', 'Omschrijving', 'ParentID',
              'AanmakerID', 'GeldigVan', 'GeldigTot', 'Actief']
    success_url = reverse_lazy('projecten')


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projecten')


def abonnementen(request):
    abonnementen = Abonnement.objects.all()
    context = {'abonnementen': abonnementen, }
    return render(request, 'abonnement.html', context=context)


class AbonnementCreate(CreateView):
    model = Abonnement
    fields = ['PersoonID', 'ProjectID', 'OriginalObjectID']
    success_url = reverse_lazy('abonnementen')


@login_required
def urenschrijven(request):

    # Dit moet een veld worden in Persoon (laatst bezochte week)
    datum = date.today()

    if request.method == 'POST':
        # form = tijdschrijfForm(request.POST)
        # if form.is_valid():
        verwerkUren.walkTheGrid(request.POST, request.user.id)

        if request.POST['weeknummer']:
            weeknummer = request.POST['weeknummer'].split('week:')
            weeknummer = [x.strip() for x in weeknummer]
            datum = dateFunctions.getDateRangeFromWeek(weeknummer[0], weeknummer[1])[0]

    eerstedagweek = dateFunctions.fdow(datum)
    # laatstedagweek = dateFunctions.ldow(datum)

    # datumsinweek = GeschrevenTijd.datumsinweek(eerstedagweek)
    tijdgrid = GeschrevenTijd.tijdoverzicht(eerstedagweek.isoformat()[0:10], request.user.id)

    # argument=2: de eerste twee letters van de dagen
    dagenInWeek = dateFunctions.daysInWeek(2)

    context = {'dagenindeweek': dagenInWeek,
               'tijdgrid': tijdgrid,
               'datum': datum.isoformat()[0:10],
               }

    return render(request, 'urenschrijven.html', context=context)


@login_required
def rapport(request):
    """View voor de rapportage pagina"""
    # Berekening totalen voor alle projecten voor alle medewerkers
    tot_uren_per_project = Project.objects.filter(abonnement__geschreventijd__TijdsDuur__gt=0).values('Titel').annotate(Totaal=Sum('abonnement__geschreventijd__TijdsDuur'))
    cumtot_uren_per_project = sum(tot_uren_per_project.values_list('Totaal', flat=True))
    # Berekening totalen voor alle projecten voor de ingelogde medewerker
    tot_uren_per_project_mdw = Project.objects.filter(persoon__user=request.user, abonnement__geschreventijd__TijdsDuur__gt=0).values('Titel').annotate(Totaal=Sum('abonnement__geschreventijd__TijdsDuur'))
    cumtot_uren_per_project_mdw = sum(tot_uren_per_project_mdw.values_list('Totaal', flat=True))
    # Berekening totalen voor alle projecten voor de ingelogde medewerker voor de maand maart
    tot_uren_per_project_mdw_per = Project.objects.filter(persoon__user=request.user, abonnement__geschreventijd__Datum__range=["2021-03-01", "2021-03-31"], abonnement__geschreventijd__TijdsDuur__gt=0).values('Titel').annotate(Totaal=Sum('abonnement__geschreventijd__TijdsDuur'))
    cumtot_uren_per_project_mdw_per = sum(tot_uren_per_project_mdw_per.values_list('Totaal', flat=True))

    context = {
        'tot_uren_per_project': tot_uren_per_project,
        'cumtot_uren_per_project': cumtot_uren_per_project,
        'tot_uren_per_project_mdw': tot_uren_per_project_mdw,
        'cumtot_uren_per_project_mdw': cumtot_uren_per_project_mdw,
        'tot_uren_per_project_mdw_per': tot_uren_per_project_mdw_per,
        'cumtot_uren_per_project_mdw_per': cumtot_uren_per_project_mdw_per,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'rapport.html', context=context)
