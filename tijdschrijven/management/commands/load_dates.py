from django.core.management import BaseCommand
from tijdschrijven.models import Datumtabel
from datetime import date, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        for datum in (date(2020, 1, 1) + timedelta(n) for n in range(800)):
            dats = Datumtabel()
            dats.datum = datum
            dats.save()

        print('script uitgevoerd')
