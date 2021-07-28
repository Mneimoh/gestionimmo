from . import views
from django.urls import path


urlpatterns = [
    # path('', views.index, name='login'),
    path('', views.login_request, name="signin"),
    path('logout', views.logout_controller, name="logout")
]
