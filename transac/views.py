from django.shortcuts import render
from .decorators import unauthenticated_user,allowed_users

# Create your views here.

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def index(request):
      return render(request, 'transac/tcompte.html', { 'title': 'Espace ouverture compte'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def vente(request):
      return render(request, 'transac/tvente.html', { 'title': 'Espace vente'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def penalties(request):
      return render(request, 'transac/tpenalties.html', { 'title': 'Pénalités'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def payments(request):
      return render(request, 'transac/tpaiement.html', { 'title': 'Paiements'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def mutations(request):
      return render(request, 'transac/tmutations.html', { 'title': 'Mutations'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def restructure(request):
      return render(request, 'transac/trestructurations.html', { 'title': 'Restructurations'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def plan(request):
      return render(request, 'transac/tpml.html', { 'title': 'Plan de masse local'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac']) 
def dossiers_credit(request):
      return render(request, 'transac/tdc.html', { 'title': 'Dossiers crédits (DC)'})

@unauthenticated_user
@allowed_users(allowed_roles=['transac'])
def dossiers(request):
      return render(request, 'transac/tdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)'})


