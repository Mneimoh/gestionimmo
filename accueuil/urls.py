from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='accueuil'),
    path('rdv/', views.rdv, name='accueuil-rdv'),
    path('rdv/accueuil/api/get_appointment/', views.appointment),
    path('rdv/accueuil/api/get_appointments/', views.get_appointments),
    path('rdv/accueuil/api/paginate_appointments/', views.paginate_appointments),
]
