from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='transac'),
    path('vente', views.vente, name='vente'),
    path('penalties', views.penalties, name='penalties'),

]
