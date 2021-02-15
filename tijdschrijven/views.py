from django.shortcuts import render

# Create your views here.
from tijdschrijven .models import Persoon, Project, Abonnement, ProjectTemplate, GeschrevenTijd

def index(request):

    num_projects = Project.objects.all().count()
    #num_abonnement = Abonnement.objects.filter().count()

    context = {
        'num_projects': num_projects,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
