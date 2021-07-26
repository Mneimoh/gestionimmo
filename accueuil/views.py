from django.shortcuts import render
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
@unauthenticated_user
@allowed_users(allowed_roles=["acceuil"])
def index(request):
    return render(request,'accueuil/appel.html', { 'title': 'Enregistrement des appels'})


@unauthenticated_user
@allowed_users(allowed_roles=["acceuil"])
def rdv(request):
    return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous'})
