from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from societe.models import Agent,Societe
from authentication.models import User


admin.site.register(Societe)

# Register your models here.

class SocieteAdmin(admin.AdminSite):
    site_header = 'Societe Information'

class SetAgentPermission(admin.ModelAdmin):

    def has_add_permission(self, request: HttpRequest) -> bool:
        print('---------------------------------')
        print(request.user)
        print('---------------------------------')
        return True

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        print('---------------------------------')
        print(obj)
        print('---------------------------------')
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        print('---------------------------------')
        print(obj)
        print('---------------------------------')
        return False

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        print('---------------------------------')
        print(obj)
        print('---------------------------------')
        return True

class SetSocietePermission(admin.ModelAdmin):
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        print('------------has-add-permission---------------')
        print(request.path)
        print(request.user)
        print('---------------------------------')
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        print('-----------change---------------')
        print(request.path)
        print(request.user.societe)
        print(obj is None or obj)
        print('---------------------------------')
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        print('-----------delete----------------')
        print(request.path)
        print(obj)
        print('---------------------------------')
        return False

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        if(obj is not None):
            if(request.user.societe is obj.pk):
                return True
            else:
                return False
        return True

class SetSocieteUserPermission(admin.ModelAdmin):
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False 
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
        
societe_site = SocieteAdmin(name="Societe Admin")


societe_site.register(Agent, SetAgentPermission)
societe_site.register(User, SetSocieteUserPermission)
societe_site.register(Societe,SetSocietePermission)