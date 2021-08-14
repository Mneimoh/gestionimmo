from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='transac'),
    path('vente', views.vente, name='vente'),
    path('register/<table>/<type>/', views.registerAccount), 
    # path('register/client', views.registerAccount),
    # path('register/place', views.registerAccount),
    # path('register/emploi',  views.registerAccount),
    # path('register/endettement', views.registerAccount),
    path('mail', views.sendMail),
    path('penalties', views.penalties, name='penalties'),
    path('payments', views.payments, name='payments'),
    path('mutations', views.mutations, name='mutations'),
    path('restructure', views.restructure, name='restructure'),
    path('plan', views.plan, name='plan'),
    path('dossiers', views.dossiers, name='dossiers'),
    path('dossiers_credit', views.dossiers_credit, name='dossiers_credit'),


]
