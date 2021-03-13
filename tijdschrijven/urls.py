from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projecten', views.projecten, name='projecten'),
    path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('abonnementen', views.abonnementen, name='abonnementen'),
    path('abonnement/create/', views.AbonnementCreate.as_view(), name='abonnement-create'),
    path('urenschrijven', views.urenschrijven, name='urenschrijven'),
    path('rapportage', views.rapport, name='rapportage'),
]