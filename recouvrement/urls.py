from . import views
from django.urls import path


urlpatterns = [
    
    #Direction du recouvrement paths
    path('', views.index, name='recouvrement'),
    path('etat/', views.etat_recouvrements, name='etat_recouvrement'),
    path('contacts/', views.contacts, name='contacts'),
    path('litiges/', views.litiges, name='litiges'),
    path('finalisations/', views.finalisations, name='finalisations'),
    path('rapports/', views.rapports, name='rapports'),
    
    # Etats dossiers paths
    path('dossiers-recouvrement/', views.etat_dossiers_recouvrement, name='dossier-recouvrement'),
    path('dossiers-statistique/', views.etat_dossiers_statistique, name='dossier-statistique'),
    path('dossiers-profil/', views.etat_profil_dossiers, name='dossier-profil'),
    path('dossiers-etats-complets/', views.etat_dossiers_recouvrement_complets, name='dossier-recouvrement-etats-complets'),
    
    #Contacts paths
    path('contacts-rappel', views.contact_rappel, name='contacts-rappel'),
    path('contacts-sms', views.contact_sms, name='contacts-sms'),
    path('contacts-autosms', views.contact_autosms, name='contacts-autosms'),
    path('contacts-emails', views.contact_emails, name='contacts-emails'),
    path('contacts-autoemails', views.contact_autoemails, name='contacts-autoemails'),
    path('contacts-annotation', views.contact_annotation, name='contacts-annotation'),
    
    #Gestion Finalisation paths
    path('gestion-verification-paiement', views.gestion_verification_paiement, name='gestion-verification-paiement'),
    path('gestion-attestation', views.gestion_attestation, name='gestion-attestation'),
    path('gestion-pml', views.gestion_pml, name='gestion-pml'),
    path('gestion-felicitations', views.gestion_felicitations, name='gestion-felicitations'),
    path('gestion-attributions', views.gestion_attributions, name='gestion-attributions'),
    
    #props terriers , modif restructure path
    path('prop-terriens', views.prop_terriens, name='prop-terriens'),
    path('modif-restructure', views.modif_restructure, name='modif-restructure'),
    
    #annulation paths
    path('annulation-auto', views.annulation_auto, name='annulation-auto'),
    path('annulation-courrier', views.annulation_courrier, name='annulation-courrier'),
    path('annulation-finalisation', views.annulation_finalisation, name='annulation-finalisation'),
    
    #delocalisation paths
    path('delocalisation-auto', views.delocalisation_auto, name='delocalisation-auto'),
    path('delocalisation-courrier', views.delocalisation_courrier, name='delocalisation-courrier'),
    path('delocalisation-finalisation', views.delocalisation_finalisation, name='delocalisation-finalisation'),

    #delocalisation paths
    path('gestionpr-1', views.gestionpr_1, name='gestionpr-1'),
    path('gestionpr-2', views.gestionpr_2, name='gestionpr-2'),
    path('gestion-vi-1', views.gestion_vi_1, name='gestion-vi-1'),
    path('gestion-vi-2', views.gestion_vi_2, name='gestion-vi-2'),
    path('gestion-rejets', views.gestion_rejets, name='gestion-rejets'),
    
    #repechage paths
    path('repechage-auto', views.repechage_auto, name='repechage-auto'),
    path('repechage-2', views.repechage_2, name='repechage-2'),
]
