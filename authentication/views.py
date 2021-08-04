from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserLoginForm
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def index(request):
      print(request.user,"From base route")
      return render(request, 'authentication/login.html',{})

def login_request(request):
      error = "Invalid username or password"

      if request.method == "POST":
            form = UserLoginForm(request.POST)

            if  form.is_valid():
                  email = form.cleaned_data.get('email')
                  password = form.cleaned_data.get('password')
                  user = authenticate(email=email,password=password)

                  if user is not None:

                        if user.poste:
                        #       print('user exists')
                        #       group = request.user.groups.filter(user=request.user)[0]
                        #       login(request,user)
                        #       messages.info(request, f"You are logged in as {username}")
                        #       url = f'/{group.name}'
                        #       print(group, "From login handler")
                              # return redirect(f"/{user.poste}",context={{"user":user}})
                              request.session.set_expiry(86400) #sets the exp. value of the session 
                              login(request, user) #the user is now logged in
                              return redirect(f"/{user.poste}")
                              # return render(request=request,template_name=f"{user.poste}/{user.poste}.html",context={"user":user})
                        else:
                              error = "You are not identifired to any poste"
                  else: 
                        print(error)
                        messages.error(request,error)
            else:
                  print('Invalid form')
                  print(error)
                  messages.error(request,error)
      form = UserLoginForm()
      return render(request=request,template_name='authentication/login.html',context={"login_form":form,"error_message":error})

def logout_here(request):
      logout(request)
      return redirect("/login")
