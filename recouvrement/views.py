from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'recouvrement/recouvrement.html', { 'title': 'Recouvrement'})

def etat_recouvrements(request): 
    return render(request, 'recouvrement/direction/etat-recouvrement.html', { 'title': 'Etat des Recouvrements'})


def contacts(request): 
    return render(request, 'recouvrement/direction/gestion-contact.html', { 'title': ' Gestion des contacts'})


def litiges(request): 
    return render(request, 'recouvrement/direction/gestion-litige.html', { 'title': ' Gestion des litiges'})

def finalisations(request): 
    return render(request, 'recouvrement/direction/finalisations.html', { 'title': ' Finalisation'})

def rapports(request): 
    return render(request, 'recouvrement/direction/rapports.html', { 'title': ' Rapports'})

def etat_dossiers_recouvrement (request): 
    return render(request, 'recouvrement/etats-dossiers/recouvrement.html', { 'title': ' Etat des recouvrements'})

def etat_dossiers_statistique (request): 
    return render(request, 'recouvrement/etats-dossiers/statistique.html', { 'title': ' Etat statistique'})

def etat_profil_dossiers (request): 
    return render(request, 'recouvrement/etats-dossiers/profil-dossiers.html', { 'title': 'Profil dossiers'})

def etat_dossiers_recouvrement_complets (request): 
    return render(request, 'recouvrement/etats-dossiers/etats-complets.html', { 'title': ' Etat dossiers complets'})

