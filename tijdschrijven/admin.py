from django.contrib import admin

# Register your models here.

from .models import Persoon, Project, Abonnement, ProjectTemplate, GeschrevenTijd

admin.site.register(Persoon)

admin.site.register(Abonnement)
admin.site.register(ProjectTemplate)
# admin.site.register(GeschrevenTijd)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('Titel', 'ParentID')

class GeschrevenTijdAdmin(admin.ModelAdmin):
    list_display = ('AbonnementID', 'Datum', 'AanmaakDatum', 'TijdsDuur', )


admin.site.register(Project, ProjectAdmin)
admin.site.register(GeschrevenTijd, GeschrevenTijdAdmin)