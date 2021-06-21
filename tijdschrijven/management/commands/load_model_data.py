from csv import DictReader

from django.core.management import BaseCommand

from tijdschrijven.models import Project, Persoon, Abonnement, Projectgroep, Datumtabel, Activiteit, Project_Activiteit
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from datetime import date, timedelta, datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Project.objects.exists():
            print('Let op!!! Er staan al projecten in de database...')
            print('Voor een schone start, kun je Sqlite verwijderen en de migraties opnieuw uitvoeren.')

        print('groepdata laden')
        for row in DictReader(open('./data/groep_data.csv')):
            grp = Projectgroep()
            grp.groep = row['groep']
            grp.save()
        print('groepen geladen')

        print("Laden projectdata...")
        for row in DictReader(open('./data/project_data.csv')):
            proj = Project()
            proj.groep = Projectgroep.objects.get(pk=row['groep'])
            proj.titel = row['Titel']
            proj.omschrijving = row['Omschrijving']
            proj.aanmaker = row['AanmakerID']
            proj.geldigvan = row['GeldigVan']
            proj.geldigtot = row['GeldigTot']
            proj.actief = row['Actief']
            proj.save()
        print("Projecten toegevoegd.")   

        print("Toevoegen gebruikers....")
        for row in DictReader(open('./data/user_data.csv')):
            gebruiker = User.objects.create_user(row['Medewerker'], password=row['Password'])
            gebruiker.first_name = row['First']
            gebruiker.last_name = row['Last']
            gebruiker.is_active = row['Active']
            gebruiker.is_superuser = row['Superuser']
            gebruiker.is_staff = row['Staff']
            gebruiker.save()
            # aanvullen dienstverbanden
            prs = Persoon.objects.get(user=gebruiker)
            prs.dienstverband = row['Uren']
            prs.save()
            # toevoegen abonnementen
            prjs = Project.objects.all()
            for prj in prjs:
                abonmnt = Abonnement()
                abonmnt.project = prj
                abonmnt.persoon = prs
                abonmnt.originalobject = prj.id
                abonmnt.save()


        print("Gebruikers toegevoegd.")

        print('activiteiten toevoegen')


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

        print('datums aanmaken')

        for datum in (date(2020, 1, 1) + timedelta(n) for n in range(800)):
            dats = Datumtabel()
            dats.datum = datum
            dats.save()

        print('datums ingeladen')

        print("Het script is volledig uitgevoerd.")



