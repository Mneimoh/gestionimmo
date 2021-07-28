from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def index(request):
      print(request.user.groups.filter(user=request.user)[0])
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
                        group = None
                        if request.user.groups.exists():
                              group = request.user.groups.filter(user=request.user)[0]
                              login(request,user)
                              messages.info(request, f"You are logged in as {username}")
                              url = f'/{group.name}'
                              print(group, "From login handler")
                              return redirect(url)
                  else: 
                        print(error)
                        messages.error(request,error)
            else:
                  print(error)
                  messages.error(request,error)
      form = UserLoginForm()
      return render(request=request,template_name='authentication/signin.html',context={"login_form":form})


@login_required(login_url='login')
def logout_request(request):
      logout(request)
      messages.info(request, "Log out Successfully!!")
      return redirect('login')