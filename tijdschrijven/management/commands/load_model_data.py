from csv import DictReader

from django.core.management import BaseCommand

from tijdschrijven.models import Project
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
        for row in DictReader(open('./project_data.csv')):
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
        
        for row2 in DictReader(open('./user_data.csv')):
            gebruiker = User.objects.create_user(row2['Medewerker'], password=row2['Password'])
            gebruiker.first_name = row2['First']
            gebruiker.last_name = row2['Last']
            gebruiker.is_active = row2['Active']
            gebruiker.is_superuser= row2['Superuser']
            gebruiker.is_staff= row2['Staff']
            gebruiker.save()
        print("Gebruikers toegevoegd.")
        print("Het script is volledig uitgevoerd.")
        
        
