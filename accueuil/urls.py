from . import views
from django.urls import path


urlpatterns = [
    path('', views.upload, name='acceuil'),
    path('rdv/', views.rdv, name='acceuil-rdv')
]
