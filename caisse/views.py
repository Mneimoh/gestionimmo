from django.shortcuts import render

# Create your views here.

def index(request):
    #return render(request,'accueuil/appel.html', { 'title': 'Enregistrement des appels'})
    return render(request, 'caisse/caisse.html', {'title': 'Ouverture et montage de dossier'})

def cpaiement(request):
    return render(request,'caisse/cpaiements.html', { 'title': 'Paiements mensuels'})

def cpenalites(request):
    return render(request,'caisse/cpenalites.html', { 'title': 'Pénalités'})

def crestructurations(request):
    return render(request,'caisse/crestructurations.html', { 'title': 'Restructurations'})

def cdelocalisations(request):
    return render(request,'caisse/cdelocalisations.html', { 'title': 'Délocalisations'})

def cmutations(request):
    return render(request,'caisse/cmutations.html', { 'title': 'Mutations'})

def cpml(request):
    return render(request,'caisse/cpml.html', { 'title': 'Plan de masse local'})

def cdcpt(request):
    return render(request,'caisse/cdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)'})

def cdc(request):
    return render(request,'caisse/cdc.html', { 'title': 'Dossiers crédits (DC)'})
