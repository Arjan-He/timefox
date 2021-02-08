from django.db import models

# Create your models here.
class Persoon(models.Model):

    Naam = models.CharField(max_length=64)
    EmailAdres = models.CharField(max_length=128)
    Aanmaakdatum = models.DateField(auto_now_add=True)
    MutatieDatum = models.DateField(auto_now=True)
    #GeldigVan = models.DateField()
    #GeldigTot = models.DateField()
    Wachtwoord = models.BinaryField()

    ROL_OMS = (
        (1, 'Medewerker'),
        (2, 'Leidinggevende'),
        (3, 'Beheerder'),
    )

    rol = models.SmallIntegerField(
        choices=ROL_OMS,
        blank=True,
        default=1,
        help_text='Rolomschrijving',
    )

    Projecten = models.ManyToManyField('Project', through='Abonnement')

    class Meta:
        verbose_name_plural = "personen"

    def __str__(self):
        """String for representing the Model object."""
        return self.Naam

class AccountSetting(models.Model):
    PersoonID = models.ForeignKey('Persoon', on_delete=models.CASCADE)

    ACCOOUNTITEMS = (
        (1, 'Dienstverband'),
        #(2, 'In Dienst'),
    )

    AccountItem = models.SmallIntegerField(
        choices=ACCOOUNTITEMS,
        blank=True,
        default=1,
        help_text='Acoount item',
    )
    Setting = models.IntegerField
    AanmaakDatum = models.DateField(auto_now_add=True)
    GeldigVan = models.DateField()
    GeldigTot = models.DateField()    

    def __str__(self):
        """String for representing the Model object."""
        return self.AccountItem


class Project(models.Model):
    Titel = models.CharField(max_length=128, null=True)
    ProjectTemplateID = models.ForeignKey('ProjectTemplate', on_delete=models.RESTRICT)
    Omschrijving = models.CharField(max_length=256, null=True)
    ParentID = models.ForeignKey('self',on_delete=models.CASCADE,null=True, related_name='subproject')
    AanmaakDatum = models.DateField(auto_now_add=True)
    MutatieDatum = models.DateField(auto_now=True)
    GeldigVan = models.DateField()
    GeldigTot = models.DateField()
    Actief = models.BooleanField()
    Personen = models.ManyToManyField('Persoon', through='Abonnement')

    def __str__(self):
        """String for representing the Model object."""
        return self.Titel

class ProjectTemplate(models.Model):
    Titel = models.CharField(max_length=128)
    Omschrijving = models.CharField(max_length=256)

    def __str__(self):
        """String for representing the Model object."""
        return self.Titel

class Abonnement(models.Model):
    ProjectID = models.ForeignKey('Project', on_delete=models.CASCADE)
    PersoonID = models.ForeignKey('Persoon', on_delete=models.CASCADE) 
    OriginalObjectID = models.IntegerField()
    AanmaakDatum = models.DateField(auto_now_add=True)
    Zichtbaarheid = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "abonnementen"

class GeschrevenTijd(models.Model):
    AbonnementID = models.ForeignKey('Abonnement', on_delete=models.CASCADE)
    AanmaakDatum = models.DateField(auto_now_add=True)
    Datum = models.DateField()
    TijdsDuur = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "geschreven tijd"
