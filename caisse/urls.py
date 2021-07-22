from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='caisse'),
    path('paiements', views.cpaiement, name='cpaiements'),
    path('penalites', views.cpenalites, name='cpenalites'),
    path('restructurations', views.crestructurations, name='crestructurations'),
    path('delocalisations', views.cdelocalisations, name='cdelocalisations'),
    path('mutations', views.cmutations, name='cmutations'),
    path('cpml', views.cpml, name='cpml'),
    path('cdcpt', views.cdcpt, name='cdcpt'),
    path('cdc', views.cdc, name='cdc')
]
