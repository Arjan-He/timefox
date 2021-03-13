from csv import DictReader

from django.core.management import BaseCommand

from tijdschrijven.models import Project, Persoon, Abonnement
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



class Command(BaseCommand):
    # Show this when the user types help
    help = "Haalt data uit de csv data bestanden en laadt deze via het model in de database"

    def handle(self, *args, **options):
        if Project.objects.exists():
            print('Let op!!! Er staan al projecten in de database...')
            print('Voor een schone start, kun je Sqlite verwijderen en de migraties opnieuw uitvoeren.')
        print("Laden projectdata...")
        for row in DictReader(open('./data/project_data.csv')):
            project = Project()
            project.Titel = row['Titel']
            project.Omschrijving = row['Omschrijving']
            project.AanmakerID = row['AanmakerID']
            project.GeldigVan = row['GeldigVan']
            project.GeldigTot = row['GeldigTot']
            project.Actief= row['Actief']
            project.save()
        print("Projecten toegevoegd.")
        
       
        print("Toevoegen gebruikers....")
        
        for row in DictReader(open('./data/user_data.csv')):
            gebruiker = User.objects.create_user(row['Medewerker'], password=row['Password'])
            gebruiker.first_name = row['First']
            gebruiker.last_name = row['Last']
            gebruiker.is_active = row['Active']
            gebruiker.is_superuser= row['Superuser']
            gebruiker.is_staff= row['Staff']
            gebruiker.save()
            # aanvullen dienstverbanden
            persoon = Persoon.objects.get(user=gebruiker)
            persoon.Dienstverband=row['Uren']
            persoon.save()
            # toevoegen abonnementen
            projecten = Project.objects.all()
            for project in projecten:
                abonnement = Abonnement()
                abonnement.ProjectID=project
                abonnement.PersoonID=persoon
                abonnement.OriginalObjectID=project.id
                abonnement.save()
        print("Gebruikers toegevoegd.")
        print("Het script is volledig uitgevoerd.")
        
        
