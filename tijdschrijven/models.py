from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.widgets import DateTimeInput
# from django.conf import settings
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
# from django_cte import CTEManager


class Projectgroep(models.Model):
    groep = models.CharField(max_length=32)

    def __str__(self):
        """String for representing the Model object."""
        return self.groep

    class Meta:
        verbose_name_plural = "projectgroepen"


class Project(models.Model):
    groep = models.ForeignKey(Projectgroep, on_delete=models.CASCADE)
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
    persoon = models.ForeignKey(Persoon, on_delete=models.CASCADE)
    projectactiviteit = models.ForeignKey('Project_Activiteit', on_delete=models.CASCADE)
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
                              ,act.id as activiteitID
                              ,pac.id as projectactiviteitID
                              ,act.activiteit
                              ,prs.user_id
                              ,prj.id projectID
                              ,prj.titel
                              ,prj.groep_id groepID
                              ,pjg.groep
                              ,tyd.tijdsduur
                              ,tyd.id as tijdID


                        from weekdag wkd
                        
                        join tijdschrijven_abonnement abm
                          on 1=1
                          
                        join tijdschrijven_project prj
                          on abm.project_id = prj.id

                        join tijdschrijven_projectgroep pjg
                          on prj.groep_id = pjg.id

                        join tijdschrijven_project_activiteit pac
                          on abm.project_id = pac.project_id

                        join tijdschrijven_activiteit act
                          on pac.activiteit_id = act.id

                        join tijdschrijven_persoon prs
                          on abm.persoon_id = prs.id
                         and prs.user_id = %s

                        left join tijdschrijven_geschreventijd tyd
                          on tyd.persoon_id = prs.id
                         and tyd.projectactiviteit_id = pac.id
                         and tyd.datum = wkd.datum
                        
                        order by prj.groep_id
                                ,prj.id
                                ,pac.id
                                ,wkd.datum
                '''
        return GeschrevenTijd.objects.raw(query, [datum, prs])


    def __str__(self):
        """String for representing the Model object."""
        return self.persoon.user.first_name + " " + \
            self.persoon.user.last_name + " - " +  \
            self.projectactiviteit.project.titel + " - " +  \
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

# cte vervangen door datumtabel
# select wkd.datum
# ,abm.id as abonnementID
# 	  , case 
# 					when STRFTIME('%w',wkd.datum)='0' then 7
# 					else STRFTIME('%w',wkd.datum)
# 				 end as id	 
#  from tijdschrijven_datumtabel wkd 
 
#                         join tijdschrijven_abonnement abm
#                           on 1=1
 
# where wkd.datum >= '2021-01-04'
#   and wkd.datum < date('2021-01-04','+7 day')