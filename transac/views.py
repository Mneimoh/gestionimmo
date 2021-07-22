from django.shortcuts import render

# Create your views here.
def index(request):
      return render(request, 'transac/tcompte.html', { 'title': 'Espace ouverture compte'})

def vente(request):
      return render(request, 'transac/tvente.html', { 'title': 'Espace vente'})