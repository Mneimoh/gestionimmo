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
                  username = form.cleaned_data.get('username')
                  password = form.cleaned_data.get('password')
                  user = authenticate(username=username,password=password)
                  if user is not None:
                        login(request,user)
                        messages.info(request,f"You are now logged in as {username}")
                        group = user.groups.all()[0]
                        url = f"{group.name}/"

                        return redirect(url)
                  else:
                        messages.error(request,error)
            else:
                  print(error)
                  messages.error(request,error)
      form = UserLoginForm()
      return render(request=request,template_name='authentication/signin.html',context={"login_form":form})

def logout_controller(request):
    logout(request)
    messages.info(request, "Logged out succesfully")
    return redirect("/")

