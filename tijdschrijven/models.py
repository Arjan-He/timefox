from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings #https://learndjango.com/tutorials/django-best-practices-referencing-user-model

from django_cte import CTEManager

class Project(models.Model):
    Titel = models.CharField(max_length=88, null=True)
    ProjectTemplateID = models.ForeignKey('ProjectTemplate', on_delete=models.RESTRICT, null=True, blank=True)
    Omschrijving = models.CharField(max_length=256, null=True)
    ParentID = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='Parent')
    AanmakerID = models.IntegerField(null=True)
    AanmaakDatum = models.DateField(auto_now_add=True)
    MutatieDatum = models.DateField(auto_now=True)
    GeldigVan = models.DateField()
    GeldigTot = models.DateField()
    Actief = models.BooleanField()
    Personen = models.ManyToManyField('Persoon', through='Abonnement')
    objects = CTEManager()

    def __str__(self):
        """String for representing the Model object."""
        return self.Titel

    #rawquery voor de tree
    def geef_project_tree(project_id):
        query = '''
        WITH RECURSIVE parents AS (
            SELECT Project.*, 0 AS relative_depth
            FROM Project
            WHERE id = %s

            UNION ALL

            SELECT project.*, parents.relative_depth + 1
            FROM project,parents
            WHERE project.id = parents.parent_id
        )
        SELECT id, Titel, ParentID, relative_depth
        FROM parents
        ORDER BY relative_depth;
        '''
        return Project.objects.raw(query, [project_id])

    class Meta:
        verbose_name_plural = "projecten"


class Persoon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Dienstverband = models.IntegerField(default=0)
    Projecten = models.ManyToManyField(Project, through='Abonnement')

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
    ProjectID = models.ForeignKey(Project, on_delete=models.CASCADE)
    PersoonID = models.ForeignKey(Persoon, on_delete=models.CASCADE) 
    OriginalObjectID = models.IntegerField()
    AanmaakDatum = models.DateField(auto_now_add=True)
    Actief = models.BooleanField(default=True)
    Zichtbaarheid = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "abonnementen"

    def __str__(self):
        return self.PersoonID.user.first_name + " " + \
            self.PersoonID.user.last_name + " - " +  \
            self.ProjectID.Titel

# class AccountSetting(models.Model):
#     PersoonID = models.ForeignKey(User, on_delete=models.CASCADE)

#     ACCOOUNTITEMS = (
#         (1, 'Dienstverband'),
#     )

#     AccountItem = models.SmallIntegerField(
#         choices=ACCOOUNTITEMS,
#         blank=True,
#         default=1,
#         help_text='Acoount item',
#     )
#     Setting = models.IntegerField(null=True)
#     AanmaakDatum = models.DateField(auto_now_add=True)
#     GeldigVan = models.DateField()
#     GeldigTot = models.DateField()   

#     def __str__(self):
#         """String for representing the Model object."""
#         return self.AccountItem


class ProjectTemplate(models.Model):
    Titel = models.CharField(max_length=128)
    Omschrijving = models.CharField(max_length=256)

    def __str__(self):
        """String for representing the Model object."""
        return self.Titel


class GeschrevenTijd(models.Model):
    AbonnementID = models.ForeignKey('Abonnement', on_delete=models.CASCADE)
    AanmaakDatum = models.DateField(auto_now_add=True)
    Datum = models.DateField()
    TijdsDuur = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = "geschreven tijd"

    def tijdoverzicht(datum,prs):
        query = '''
               with recursive weekdag 
                    as (select 0 as id
                              ,%s as datum
                         union all
                        select id+1
                              ,date(datum,'+1 day') 
                          from weekdag limit 7
                        )
                        select wkd.id
                              ,prj.id as projectID
                              ,abm.id as abonnementID
                              ,tyd.id tijdID
                              ,wkd.datum 
                              ,tyd.TijdsDuur
                              ,prj.Titel
                          from weekdag wkd

                          join tijdschrijven_abonnement abm
                            on 1=1

                          join tijdschrijven_persoon prs
                            on abm.PersoonID_id = prs.id
                           and prs.user_id = %s

                          join tijdschrijven_project prj
                            on abm.ProjectID_id = prj.id

                          left join tijdschrijven_geschreventijd tyd
                            on tyd.AbonnementID_id = abm.id
                           and tyd.Datum = wkd.datum

                         order by prj.id
                                 ,abm.id
                                 ,wkd.datum;
                '''
        return GeschrevenTijd.objects.raw(query, [datum,prs])

    def __str__(self):
        """String for representing the Model object."""
        return  self.AbonnementID.PersoonID.user.first_name + " " + \
            self.AbonnementID.PersoonID.user.last_name + " - " +  \
            self.AbonnementID.ProjectID.Titel + " - " +  \
            str(self.Datum) + " - " + str(self.TijdsDuur)

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

 