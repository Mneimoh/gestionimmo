from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, allowed_users
# Create your views here.


section = 'caisse'

@login_required
def index(request):
    if(request.user.poste == section):
        return render(request, 'caisse/caisse.html', {'title': 'Ouverture et montage de dossier'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cpaiement(request):
    if(request.user.poste == section):
        return render(request,'caisse/cpaiements.html', { 'title': 'Paiements mensuels'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cpenalites(request):
    if(request.user.poste == section):
        return render(request,'caisse/cpenalites.html', { 'title': 'Pénalités'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def crestructurations(request):
    if(request.user.poste == section):
        return render(request,'caisse/crestructurations.html', { 'title': 'Restructurations'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cdelocalisations(request):
    if(request.user.poste == section):
        return render(request,'caisse/cdelocalisations.html', { 'title': 'Délocalisations'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cmutations(request):
    if(request.user.poste == section):
        return render(request,'caisse/cmutations.html', { 'title': 'Mutations'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cpml(request):
    if(request.user.poste == section):
        return render(request,'caisse/cpml.html', { 'title': 'Plan de masse local'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cdcpt(request):
    if(request.user.poste == section):
        return render(request,'caisse/cdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)'})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cdc(request):
    if(request.user.poste == section):
        return render(request,'caisse/cdc.html', { 'title': 'Dossiers crédits (DC)'})
    else:
        return redirect(f"/login?next=/{section}/")
