from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='acceuil'),
    path('rdv/', views.rdv, name='acceuil-rdv')
]
