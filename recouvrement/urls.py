from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='recouvrement'),
    path('etat/', views.etat_recouvrements, name='etat_recouvrement'),
    path('contacts/', views.contacts, name='contacts'),
    path('litiges/', views.litiges, name='litiges'),
    path('finalisations/', views.finalisations, name='finalisations'),
    path('rapports/', views.rapports, name='rapports'),
    path('dossiers-recouvrement/', views.etat_dossiers_recouvrement, name='dossier-recouvrement'),
    path('dossiers-statistique/', views.etat_dossiers_statistique, name='dossier-statistique'),
    path('dossiers-profil/', views.etat_profil_dossiers, name='dossier-profil'),
    path('dossiers-etats-complets/', views.etat_dossiers_recouvrement_complets, name='dossier-recouvrement-etats-complets'),
]

