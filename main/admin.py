from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ('societe', 'nom', 'prenom', 'statut','created_at')
    list_filter = ("statut","created_at","nom")
    search_fields = ['societe', 'content']
    
admin.site.register(Agent, AgentAdmin )
app_models = apps.get_app_config('main').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
