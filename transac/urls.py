from . import views
from django.urls import path


urlpatterns = [
    path('', views.prequalifList , name='transac'),
    path('transac/api/pay_facture',views.pay_facture),
    path('facture/api/get_facture', views.get_facture),
    path('compte/<nom>',views.index, name="transact list"),
    path('vente', views.vente, name='vente'),
    path('register/<table>/<type>/', views.registerAccount),
    path('generatepdf/<name>/', views.makePdf),
    path('credit/<dossier>/', views.save_credit),
    # path('register/client', views.registerAccount),
    # path('register/place', views.registerAccount),
    # path('register/emploi',  views.registerAccount),
    # path('register/endettement', views.registerAccount),
    path('mail', views.sendMail),
    path('penalties', views.penalties, name='penalties'),
    path('penalites/api/get_penalites', views.get_penalite),
    path('penalites/api/paginate_penalites', views.paginate_penalite),
    path('penalites/api/set_facture_amount', views.set_facture_penalty),
    path('payments', views.payments, name='payments'),
    path('paiements/api/get_paiements', views.get_paiement),
    path('paiements/api/paginate_paiements', views.paginate_paiement),
    path('mutations', views.mutations, name='mutations'),
    path('mutations/api/get_mutations', views.get_mutations),
    path('mutations/api/paginate_mutations', views.paginate_mutations),
    path('restructure', views.restructure, name='restructure'),
    path('restructurations/api/get_restructurations', views.get_restructurations),
    path('restructurations/api/paginate_restructurations', views.paginate_restructurations),
    path('plan', views.plan, name='plan'),
    path('tpml/api/get_tpml', views.get_tpml),
    path('tpml/api/paginate_tpml', views.paginate_tpml),
    path('dossiers', views.dossiers, name='dossiers'),
    path('tdcpt/api/get_tdcpt', views.get_tdcpt),
    path('tdcpt/api/paginate_tdcpt', views.paginate_tdcpt),
    path('dossiers_credit', views.dossiers_credit, name='dossiers_credit'),
    path('tdc/api/get_tdc', views.get_tdc),
    path('tdc/api/paginate_tdc', views.paginate_tdc)

]
