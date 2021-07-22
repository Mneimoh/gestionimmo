from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='transac'),
    path('vente', views.vente, name='vente'),
    path('penalties', views.penalties, name='penalties'),
    path('payments', views.payments, name='payments'),
    path('mutations', views.mutations, name='mutations'),
    path('restructure', views.restructure, name='restructure'),


]
