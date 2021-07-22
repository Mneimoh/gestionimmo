from django.shortcuts import render

# Create your views here.
def index(request):
      return render(request, 'transac/tcompte.html', { 'title': 'Espace ouverture compte'})

def vente(request):
      return render(request, 'transac/tvente.html', { 'title': 'Espace vente'})

def penalties(request):
      return render(request, 'transac/tpenalties.html', { 'title': 'Pénalités'})

def payments(request):
      return render(request, 'transac/tpaiement.html', { 'title': 'Paiements'})

def mutations(request):
      return render(request, 'transac/tmutations.html', { 'title': 'Mutations'})

def restructure(request):
      return render(request, 'transac/trestructurations.html', { 'title': 'Restructurations'})

def plan(request):
      return render(request, 'transac/tpml.html', { 'title': 'Plan de masse local'})

def dossiers(request):
      return render(request, 'transac/tdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)'})

