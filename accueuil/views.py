from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

section = "accueuil"
# Create your views here.

@login_required
def index(request):
    if(request.user.poste == section):
        return render(request,'accueuil/appel.html', { 'title': 'Enregistrement des appels'})
    else:
        return redirect(f"/login?next=/{section}/")

@login_required
def rdv(request):
    if(request.user.poste == section):
        return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous'})
    else:
        return redirect(f"/login?next=/{section}/")
