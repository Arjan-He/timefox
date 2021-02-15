from django.contrib import admin

# Register your models here.

from .models import Persoon, Project, Abonnement, ProjectTemplate, GeschrevenTijd

admin.site.register(Persoon)
admin.site.register(Project)
admin.site.register(Abonnement)
admin.site.register(ProjectTemplate)
admin.site.register(GeschrevenTijd)