from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users

# Create your views here.
section = 'transac'


@login_required
def index(request):
      if(request.user.poste == section):
            return render(request, 'transac/tcompte.html', { 'title': 'Espace ouverture compte'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def vente(request):
      if(request.user.poste == section):
            return render(request, 'transac/tvente.html', { 'title': 'Espace vente'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def penalties(request):
      if(request.user.poste == section):
            return render(request, 'transac/tpenalties.html', { 'title': 'Pénalités'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def payments(request):
      if(request.user.poste == section):
            return render(request, 'transac/tpaiement.html', { 'title': 'Paiements'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def mutations(request):
      if(request.user.poste == section):
            return render(request, 'transac/tmutations.html', { 'title': 'Mutations'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def restructure(request):
      if(request.user.poste == section):
            return render(request, 'transac/trestructurations.html', { 'title': 'Restructurations'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def plan(request):
      if(request.user.poste == section):
            return render(request, 'transac/tpml.html', { 'title': 'Plan de masse local'})
      else:
            return redirect(f"/login?next=/{section}/")




# @login_required 
def dossiers_credit(request):
      if(request.user.poste == section):
            return render(request, 'transac/tdc.html', { 'title': 'Dossiers crédits (DC)'})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def dossiers(request):
      if(request.user.poste == section):
            return render(request, 'transac/tdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)'})
      else:
            return redirect(f"/login?next=/{section}/")



