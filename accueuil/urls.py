from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='accueil'),
    path('rdv/', views.rdv, name='accueil-rdv')
]
