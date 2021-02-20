from django.contrib import admin

# Register your models here.

from .models import Persoon, Project, Abonnement, ProjectTemplate, GeschrevenTijd

admin.site.register(Persoon)

admin.site.register(Abonnement)
admin.site.register(ProjectTemplate)
admin.site.register(GeschrevenTijd)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('Titel', 'ParentID')


admin.site.register(Project, ProjectAdmin)