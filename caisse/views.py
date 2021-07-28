from django.shortcuts import render
from .decorators import unauthenticated_user, allowed_users
# Create your views here.

@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def index(request):
    return render(request, 'caisse/caisse.html', {'title': 'Ouverture et montage de dossier'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cpaiement(request):
    return render(request,'caisse/cpaiements.html', { 'title': 'Paiements mensuels'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cpenalites(request):
    return render(request,'caisse/cpenalites.html', { 'title': 'Pénalités'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def crestructurations(request):
    return render(request,'caisse/crestructurations.html', { 'title': 'Restructurations'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cdelocalisations(request):
    return render(request,'caisse/cdelocalisations.html', { 'title': 'Délocalisations'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cmutations(request):
    return render(request,'caisse/cmutations.html', { 'title': 'Mutations'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cpml(request):
    return render(request,'caisse/cpml.html', { 'title': 'Plan de masse local'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cdcpt(request):
    return render(request,'caisse/cdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)'})


@unauthenticated_user
@allowed_users(allowed_roles=["caisse"])
def cdc(request):
    return render(request,'caisse/cdc.html', { 'title': 'Dossiers crédits (DC)'})
