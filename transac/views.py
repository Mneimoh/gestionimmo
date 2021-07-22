from django.shortcuts import render

# Create your views here.
def index(request):
      return render(request, 'transac/tcompte.html', { 'title': 'Espace ouverture compte'})