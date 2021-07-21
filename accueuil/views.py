from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'accueuil/appel.html', { 'title': 'Enregistrement des appels'})

def rdv(request):
    return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous'})
