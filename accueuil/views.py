from django.shortcuts import render
from .decorators import unauthenticated_user, allowed_users
from .forms import ClientRdv


# Create your views here.
@unauthenticated_user
@allowed_users(allowed_roles=["acceuil"])
def index(request):
    form = ClientRdv()
    return render(request = request, template_name= 'accueuil/appel.html', context= { 'client_form': form, 'title': 'Enregistrement des appels'})


@unauthenticated_user
@allowed_users(allowed_roles=["acceuil"])
def rdv(request):
    return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous'})
