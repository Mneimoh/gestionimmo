from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .decorators import unauthenticated_user, allowed_users
from .forms import ClientCreate, ClientRdv


# Create your views here.
@unauthenticated_user
@allowed_users(allowed_roles=["acceuil"])
def index(request):
    form = ClientRdv()
    appel = ClientCreate()
    if request.method == 'POST':
        appel = ClientCreate(request.POST, request.FILES)
        form = ClientRdv(request.POST, request.FILES)
        if appel.is_valid() and form.is_valid():
            appel.save()
            form.save()
            print("everthing saved")
            return redirect('accueuil/rdv.html')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'accueuil/appel.html'}}">reload</a>""")
    else:
        form = ClientRdv()
        appel = ClientCreate()

    return render(request = request, template_name= 'accueuil/appel.html', context= { 'client_form': form, 'client_form1': appel,  'title': 'Enregistrement des appels'})


@unauthenticated_user
@allowed_users(allowed_roles=["acceuil"])
def rdv(request):
    return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous'})




