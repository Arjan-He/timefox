from django.contrib import admin

# Register your models here.

from .models import Persoon, Project, Abonnement, Project_Activiteit, GeschrevenTijd

admin.site.register(Persoon)

admin.site.register(Abonnement)
admin.site.register(Project_Activiteit)
# admin.site.register(GeschrevenTijd)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titel',)


class GeschrevenTijdAdmin(admin.ModelAdmin):
    list_display = ('persoon', 'datum', 'aanmaakdatum', 'tijdsduur', )


admin.site.register(Project, ProjectAdmin)
admin.site.register(GeschrevenTijd, GeschrevenTijdAdmin)
