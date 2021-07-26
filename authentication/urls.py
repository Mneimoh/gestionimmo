from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='login'),
    path('login', views.login_request, name="signin")
]
