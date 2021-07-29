from django.shortcuts import render, redirect
from main.models import ClientAppel
from .forms import AcceuilCreate
from django.http import HttpResponse
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

# CRUD functionalities

def acceuil_data(request):
    acceuil = ClientAppel.objects.all()
    return render(request, 'accueuil/rdv.html', {'title': acceuil})



def upload(request):
    upload = AcceuilCreate()
    if request.method == 'POST':
        upload = AcceuilCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('accueuil/rdv.html')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request=request,template_name= 'accueuil/appel.html', context={'upload_form': upload})



   