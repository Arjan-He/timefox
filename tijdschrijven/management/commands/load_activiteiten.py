from csv import DictReader

from django.core.management import BaseCommand

from tijdschrijven.models import Activiteit,Project_Activiteit, Project
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date, timedelta, datetime


class Command(BaseCommand):
    def handle(self, *args, **options):

        if Activiteit.objects.exists():
             print('Let op!!! Er staan al activiteiten in de database...')
             print('Voor een schone start, kun je Sqlite verwijderen en de migraties opnieuw uitvoeren.')

        print("Laden activiteiten ...")
        for row in DictReader(open('./data/activiteit_data.csv')):
            act = Activiteit()
            act.activiteit = row['activiteit']
            act.omschrijving = row['omschrijving']
            act.save()
        print("activiteiten toegevoegd.")

        print("Laden project_activiteiten ...")
        for row in DictReader(open('./data/project_activiteit_data.csv')):
            pact = Project_Activiteit()
            prjs = Project.objects.get(pk=row['project'])
            pact.project = prjs
            pa = Activiteit.objects.get(pk=row['activiteit'])
            pact.activiteit = pa
            pact.save()

        print("project_activiteiten toegevoegd.")

        print("Het script is volledig uitgevoerd.")



