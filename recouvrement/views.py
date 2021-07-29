from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
# Direction du recouvrement routes
# @unauthenticated_user
# @allowed_users(allowed_roles=['recouvrement'])
section = "recouvrement"

@login_required
def index(request):
    if(request.user.poste == section):
        return render(request,'recouvrement/recouvrement.html', { 'title': 'Recouvrement'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def etat_recouvrements(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/etat-recouvrement.html', { 'title': 'Etat des Recouvrements'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def contacts(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/gestion-contact.html', { 'title': ' Gestion des contacts'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def litiges(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/gestion-litige.html', { 'title': ' Gestion des litiges'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def finalisations(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/finalisations.html', { 'title': ' Finalisation'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def rapports(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/rapports.html', { 'title': ' Rapports'})
    else:
        return redirect(f"/login?next=/{section}/")


# Etats dossiers routes

@login_required
def etat_dossiers_recouvrement (request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/recouvrement.html', { 'title': ' Etat des recouvrements'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def etat_dossiers_statistique (request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/statistique.html', { 'title': ' Etat statistique'})
    else:
        return redirect(f"/login?next=/{section}/")

@login_required
def etat_profil_dossiers (request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/profil-dossiers.html', { 'title': 'Profil dossiers'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def etat_dossiers_recouvrement_complets (request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/etats-complets.html', { 'title': ' Etat dossiers complets'})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# Contact routes
def contact_rappel(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/rappel.html', { 'title': ' Appel Manuels'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def contact_sms(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/sms.html', { 'title': ' SMS Manuels'})
    else:
        return redirect(f"/login?next=/{section}/")

@login_required
def contact_autosms(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/autosms.html', { 'title': 'Auto SMS'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def contact_emails(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/emails.html', { 'title': ' Email Manuels'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def contact_autoemails(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/autoemails.html', { 'title': ' Auto Email'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def contact_annotation(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/annotation.html', { 'title': ' Annotation'})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# Gestion finalisation routes
def gestion_verification_paiement(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/verification-paiement.html', { 'title': 'Verification de fin de paiement'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_attestation(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/attestation.html', { 'title': ' Attestion de fin de paiement'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_pml(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/pml.html', { 'title': 'Emissions plans de masses locaux'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_felicitations(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/felicitations.html', { 'title': 'Certificats de félicitations'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_attributions(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/attributions.html', { 'title': "Certificats d'attributions"})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# (proprieraires terriens, modif restructure) routes
def prop_terriens(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/credit-prop-terriens.html', { 'title': "Dossiers crédits prop. terriens"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def modif_restructure(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/modif-restructure.html', { 'title': "Modification & Restructuration"})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# annulation routes
def annulation_auto(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/annulation/automatique.html', { 'title': "Annulation automatique"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def annulation_courrier(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/annulation/courrier.html', { 'title': "Annulation par courrier"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def annulation_finalisation(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/annulation/finalisation.html', { 'title': "Annulation finalisation"})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# delocalisation routes
def delocalisation_auto(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/delocalisation/automatique.html', { 'title': "Delocalisation automatique"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def delocalisation_courrier(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/delocalisation/courrier.html', { 'title': "Delocalisation par courrier"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def delocalisation_finalisation(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/delocalisation/finalisation.html', { 'title': "Delocalisation finalisation"})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# sinistre routes
def gestionpr_1(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestionpr-1.html', { 'title': "Gestion sinistre phase 1 (Reception sinistre et recherche)"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestionpr_2(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestionpr-2.html', { 'title': "Gestion sinistre phase 2 (acceptée)"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_vi_1(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestion-vi-1.html', { 'title': "Gestion sinistre phase 1 (Reception sinistre et recherche)"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_vi_2(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestion-vi-1.html', { 'title': "Gestion sinistre phase 2 (acceptée)"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def gestion_rejets(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestion-rejets.html', { 'title': "Gestion sinistre phase 2 (rejetée)"})
    else:
        return redirect(f"/login?next=/{section}/")




@login_required# repechage routes
def repechage_auto(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/repechage/automatique.html', { 'title': "Repêchage 1"})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def repechage_2(request): 
    if(request.user.poste == section):
        return render(request, 'recouvrement/repechage/repechage2.html', { 'title': "Repêchage 2"})
    else:
        return redirect(f"/login?next=/{section}/")

