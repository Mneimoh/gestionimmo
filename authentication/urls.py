from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='login'),
    path('login', views.index, name='Logout'),
    path('logout', views.logout_here, name='login'),
    path('login_request', views.login_request, name="signin")
]
