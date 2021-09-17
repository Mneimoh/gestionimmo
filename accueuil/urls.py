from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='acceuil'),
    path('rdv/', views.rdv, name='acceuil-rdv'),
    path('rdv/acceuil/api/get_appointment/', views.appointment),
    path('rdv/acceuil/api/get_appointments/', views.get_appointments),
    path('rdv/acceuil/api/paginate_appointments/', views.paginate_appointments),
]
