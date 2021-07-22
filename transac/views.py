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