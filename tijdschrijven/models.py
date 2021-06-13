from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.widgets import DateTimeInput
# from django.conf import settings
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
# from django_cte import CTEManager


class Project(models.Model):
    GROEPEN = ((1, 'overhead'),
                (3, 'onderzoek'),
                (4, 'database'),
                (5, 'rapportage'),
                (2, 'afwezigheid'))
    groep = models.IntegerField(choices=GROEPEN)
    titel = models.CharField(max_length=88, null=True)
    omschrijving = models.CharField(max_length=256, null=True)
    aanmaker = models.IntegerField(null=True)
    # lees: https://stackoverflow.com/questions/41595364/fields-e304-reverse-accessor-clashes-in-django
    aanmaakdatum = models.DateField(auto_now_add=True)
    mutatiedatum = models.DateField(auto_now=True)
    geldigvan = models.DateField()
    geldigtot = models.DateField()
    actief = models.BooleanField()
    personen = models.ManyToManyField('persoon', through='abonnement')

    def __str__(self):
        """String for representing the Model object."""
        return self.titel

    class Meta:
        verbose_name_plural = "projecten"


class Persoon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dienstverband = models.IntegerField(default=0)
    projecten = models.ManyToManyField(Project, through='Abonnement')

    class Meta:
        verbose_name_plural = "personen"

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Persoon.objects.create(user=instance)
    instance.persoon.save()


class Abonnement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    persoon = models.ForeignKey(Persoon, on_delete=models.CASCADE)
    original_project_activiteit = models.IntegerField(null=True)
    aanmaakDatum = models.DateField(auto_now_add=True)
    actief = models.BooleanField(default=True)
    zichtbaarheid = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "abonnementen"

    def __str__(self):
        return self.persoon.user.first_name + " " + \
            self.persoon.user.last_name + " - " +  \
            self.project.titel


class Activiteit(models.Model):
    activiteit = models.CharField(max_length=128)
    omschrijving = models.CharField(max_length=256)

    def __str__(self):
        """String for representing the Model object."""
        return self.activiteit

    class Meta:
        verbose_name_plural = "activiteiten"


class Project_Activiteit(models.Model):
    activiteit = models.ForeignKey(Activiteit, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "projectactiviteiten"


class GeschrevenTijd(models.Model):
    abonnement = models.ForeignKey('Abonnement', on_delete=models.CASCADE)
    aanmaakdatum = models.DateField(auto_now_add=True)
    datum = models.DateField()
    tijdsduur = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = "geschreven tijd"

    def tijdoverzicht(datum, prs):
        query = '''
                 with recursive weekdag
                    as (select 1 as id, %s as datum
                        union all
                        select id+1, date(datum,'+1 day')
                        from weekdag limit 7
                        )
                        select wkd.id
                              ,wkd.datum
                              ,abm.id as abonnementID
                              ,prs.user_id
                              ,prj.titel
                              ,tyd.tijdsduur
                              ,tyd.id as tijdID
                        from weekdag wkd
                        
                        join tijdschrijven_abonnement abm
                          on 1=1
                          
                        join tijdschrijven_project prj
                          on abm.project_id = prj.id

                        join tijdschrijven_project_activiteit pac
                          on abm.project_id = pac.project_id

                        join tijdschrijven_activiteit act
                          on pac.activiteit_id = act.id

                        join tijdschrijven_persoon prs
                          on abm.persoon_id = prs.id
                         and prs.user_id = %s 

                        left join tijdschrijven_geschreventijd tyd
                          on tyd.abonnement_id = abm.id
                         and tyd.datum = wkd.datum
                        
                        order by groep
                                ,prj.id
                                ,act.id
                '''
        return GeschrevenTijd.objects.raw(query, [datum, prs])

    def __str__(self):
        """String for representing the Model object."""
        return self.abonnement.persoon.user.first_name + " " + \
            self.abonnement.persoon.user.last_name + " - " +  \
            self.abonnement.project.titel + " - " +  \
            str(self.datum) + " - " + str(self.tijdsduur)

    def datumsinweek(datum):
        query = '''
                with recursive weekdag
                    as (select 1 as id, %s as datum
                        union all
                        select id+1, date(datum,'+1 day')
                        from weekdag limit 7
                        )
                        select wkd.id
                              ,wkd.datum
                        from weekdag wkd;
                '''
        return GeschrevenTijd.objects.raw(query, [datum])


class Datumtabel(models.Model):
    datum = models.DateField()
