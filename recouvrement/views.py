from django.shortcuts import render
from .decorators import unauthenticated_user, allowed_users
# Direction du recouvrement routes
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def index(request):
    return render(request,'recouvrement/recouvrement.html', { 'title': 'Recouvrement'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def etat_recouvrements(request): 
    return render(request, 'recouvrement/direction/etat-recouvrement.html', { 'title': 'Etat des Recouvrements'})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def contacts(request): 
    return render(request, 'recouvrement/direction/gestion-contact.html', { 'title': ' Gestion des contacts'})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def litiges(request): 
    return render(request, 'recouvrement/direction/gestion-litige.html', { 'title': ' Gestion des litiges'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def finalisations(request): 
    return render(request, 'recouvrement/direction/finalisations.html', { 'title': ' Finalisation'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def rapports(request): 
    return render(request, 'recouvrement/direction/rapports.html', { 'title': ' Rapports'})

# Etats dossiers routes
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def etat_dossiers_recouvrement (request): 
    return render(request, 'recouvrement/etats-dossiers/recouvrement.html', { 'title': ' Etat des recouvrements'})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def etat_dossiers_statistique (request): 
    return render(request, 'recouvrement/etats-dossiers/statistique.html', { 'title': ' Etat statistique'})

def etat_profil_dossiers (request): 
    return render(request, 'recouvrement/etats-dossiers/profil-dossiers.html', { 'title': 'Profil dossiers'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def etat_dossiers_recouvrement_complets (request): 
    return render(request, 'recouvrement/etats-dossiers/etats-complets.html', { 'title': ' Etat dossiers complets'})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# Contact routes
def contact_rappel(request): 
    return render(request, 'recouvrement/contacts/rappel.html', { 'title': ' Appel Manuels'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def contact_sms(request): 
    return render(request, 'recouvrement/contacts/sms.html', { 'title': ' SMS Manuels'})

def contact_autosms(request): 
    return render(request, 'recouvrement/contacts/autosms.html', { 'title': 'Auto SMS'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def contact_emails(request): 
    return render(request, 'recouvrement/contacts/emails.html', { 'title': ' Email Manuels'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def contact_autoemails(request): 
    return render(request, 'recouvrement/contacts/autoemails.html', { 'title': ' Auto Email'})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def contact_annotation(request): 
    return render(request, 'recouvrement/contacts/annotation.html', { 'title': ' Annotation'})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# Gestion finalisation routes
def gestion_verification_paiement(request): 
    return render(request, 'recouvrement/gestion-finalisation/verification-paiement.html', { 'title': 'Verification de fin de paiement'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_attestation(request): 
    return render(request, 'recouvrement/gestion-finalisation/attestation.html', { 'title': ' Attestion de fin de paiement'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_pml(request): 
    return render(request, 'recouvrement/gestion-finalisation/pml.html', { 'title': 'Emissions plans de masses locaux'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_felicitations(request): 
    return render(request, 'recouvrement/gestion-finalisation/felicitations.html', { 'title': 'Certificats de félicitations'})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_attributions(request): 
    return render(request, 'recouvrement/gestion-finalisation/attributions.html', { 'title': "Certificats d'attributions"})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# (proprieraires terriens, modif restructure) routes
def prop_terriens(request): 
    return render(request, 'recouvrement/credit-prop-terriens.html', { 'title': "Dossiers crédits prop. terriens"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def modif_restructure(request): 
    return render(request, 'recouvrement/modif-restructure.html', { 'title': "Modification & Restructuration"})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# annulation routes
def annulation_auto(request): 
    return render(request, 'recouvrement/annulation/automatique.html', { 'title': "Annulation automatique"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def annulation_courrier(request): 
    return render(request, 'recouvrement/annulation/courrier.html', { 'title': "Annulation par courrier"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def annulation_finalisation(request): 
    return render(request, 'recouvrement/annulation/finalisation.html', { 'title': "Annulation finalisation"})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# delocalisation routes
def delocalisation_auto(request): 
    return render(request, 'recouvrement/delocalisation/automatique.html', { 'title': "Delocalisation automatique"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def delocalisation_courrier(request): 
    return render(request, 'recouvrement/delocalisation/courrier.html', { 'title': "Delocalisation par courrier"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def delocalisation_finalisation(request): 
    return render(request, 'recouvrement/delocalisation/finalisation.html', { 'title': "Delocalisation finalisation"})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# sinistre routes
def gestionpr_1(request): 
    return render(request, 'recouvrement/sinistre/gestionpr-1.html', { 'title': "Gestion sinistre phase 1 (Reception sinistre et recherche)"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestionpr_2(request): 
    return render(request, 'recouvrement/sinistre/gestionpr-2.html', { 'title': "Gestion sinistre phase 2 (acceptée)"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_vi_1(request): 
    return render(request, 'recouvrement/sinistre/gestion-vi-1.html', { 'title': "Gestion sinistre phase 1 (Reception sinistre et recherche)"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_vi_2(request): 
    return render(request, 'recouvrement/sinistre/gestion-vi-1.html', { 'title': "Gestion sinistre phase 2 (acceptée)"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def gestion_rejets(request): 
    return render(request, 'recouvrement/sinistre/gestion-rejets.html', { 'title': "Gestion sinistre phase 2 (rejetée)"})

@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
# repechage routes
def repechage_auto(request): 
    return render(request, 'recouvrement/repechage/automatique.html', { 'title': "Repêchage 1"})
@unauthenticated_user
@allowed_users(allowed_roles=['recouvrement'])
def repechage_2(request): 
    return render(request, 'recouvrement/repechage/repechage2.html', { 'title': "Repêchage 2"})
