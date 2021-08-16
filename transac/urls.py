from . import views
from django.urls import path


urlpatterns = [
    path('', views.prequalifList , name='transac'),
    path('compte/<nom>',views.index, name="transact list"),
    path('vente', views.vente, name='vente'),
    path('register/<table>/<type>/', views.registerAccount),
    path('generatepdf/<name>/',views.makePdf),
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
