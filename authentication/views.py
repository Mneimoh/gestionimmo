from django.shortcuts import render,redirect
from .forms import UserLoginForm
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def index(request):
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
                              group = request.user.groups.all()[0].name
                              login(request,user)
                              messages.info(request, f"You are logged in as {username}")
                              print(group, "From login handler")
                              url = f'/{group}'
                              return redirect(url)
                  else: 
                        print(error)
                        messages.error(request,error)
            else:
                  print(error)
                  messages.error(request,error)
      form = UserLoginForm()
      return render(request=request,template_name='authentication/signin.html',context={"login_form":form})