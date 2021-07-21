from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='accueuil'),
    path('rdv/', views.rdv, name='accueuil-rdv')
]
