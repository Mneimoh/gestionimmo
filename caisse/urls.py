from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='caisse'),
    path('caisse/api/paginate_caisse', views.paginate_caisse),
    path('caisse/api/get_caisse/', views.get_caisse),
    path('caisse/api/pay_facture',views.pay_facture_om),
    path('caisse/api/genarate_facture', views.genarate_facture),
    path('paiements', views.cpaiement, name='cpaiements'),
    path('paiements/api/get_paiements', views.get_paiement),
    path('paiements/api/paginate_paiements', views.paginate_paiement),
    path('penalites', views.cpenalites, name='cpenalites'),
    path('penalites/api/get_penalites', views.get_penalite),
    path('penalites/api/paginate_penalites', views.paginate_penalite),
    path('restructurations', views.crestructurations, name='crestructurations'),
    path('restructurations/api/get_restructurations', views.get_restructurations),
    path('restructurations/api/paginate_restructurations', views.paginate_restructurations),
    path('delocalisations', views.cdelocalisations, name='cdelocalisations'),
    path('delocalisations/api/get_delocalisations', views.get_delocalisations),
    path('delocalisations/api/paginate_delocalisations', views.paginate_delocalisations),
    path('mutations', views.cmutations, name='cmutations'),
    path('mutations/api/get_mutations', views.get_mutations),
    path('mutations/api/paginate_mutations', views.paginate_mutations),
    path('cpml', views.cpml, name='cpml'),
    path('cpml/api/get_cpml', views.get_cpml),
    path('cpml/api/paginate_cpml', views.paginate_cpml),
    path('cdcpt', views.cdcpt, name='cdcpt'),
    path('cdcpt/api/get_cdcpt', views.get_cdcpt),
    path('cdcpt/api/paginate_cdcpt', views.paginate_cdcpt),
    path('cdc', views.cdc, name='cdc'),
    path('cdc/api/get_cdc', views.get_cdc),
    path('cdc/api/paginate_cdc', views.paginate_cdc),
    path('facture/api/get_facture', views.get_facture)
    
]
