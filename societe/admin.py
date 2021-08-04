from django.db import models
from django.http import request
from main.models import Article, Client, CompteEndettement, Dossier, Emploi, Endettement, PretEndettement
import societe
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest
from django.db.models import QuerySet
from main.models import Place, Societe
from main.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        # print('---------saving New User-----------------')
        # print(user)
        # print(user.societe)
        
        # print('-------------------------------------------')
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ( 'password','email', 'username', 'is_active', 'is_admin','societe','poste')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



# Register your models here.

class Administrator(admin.ModelAdmin):
    list_display        = ('username','email','date_joined','last_login','is_admin','is_staff')
    search_fields       = ('email', 'username')
    readonly_fields     = ('id','date_joined','last_login')
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()
    
class SocieteAdmin(admin.AdminSite):
    site_header = 'Societe Information'


societe_site = SocieteAdmin(name="Societe Admin")


class SetSocietePermission(UserAdmin):
    list_display        = ('nom','localisation','date_created')
    search_fields       = ('nom','active')
    readonly_fields     = ('id','date_created')
    filter_horizontal   = ()
    list_filter         = ()
    ordering            = (['nom'])
    fieldsets           = ()

    def get_queryset(self, request):

        des_societe = Societe.objects.filter(nom = request.user.societe)   
        return des_societe
            
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:

        if(obj is not None):
            if(f'{request.user.societe}' == f'{obj}'):
                return True
            else:
                return False
        return True

class SetSocieteUserPermission(BaseUserAdmin):
    list_display        = ('username','email','societe','poste','last_login','is_staff')
    search_fields       = ('poste', 'username')
    readonly_fields     = ('id','date_joined','last_login')
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()
    form                = UserChangeForm
    add_form            = UserCreationForm


    def get_queryset(self, request):
        User = get_user_model()
        print((request.user.societe and  request.user.email))
        users = User.objects.filter(societe = request.user.societe, is_admin=False)    
        return users  

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        form.base_fields['username'].initial = 'default'
 
        if not is_superuser:    
            if 'societe' in form.base_fields:
                form.base_fields['societe'].initial = 2
            disabled_fields |= {
                'is_admin',
                'is_superuser',
                'is_staff'
                # 'societe'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                print(f)
                form.base_fields[f].disabled = True
            

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'username',
                'is_superuser',
                'groups',
                'user_permissions',
                # 'societe'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
                
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        
        # if(obj is not None):
        #     print('-----------------------------------------')
        #     print(f'Societe to be changed is: {obj.societe}')
        #     print('-----------------------------------------')
        
        #     if(obj.is_admin or request.user.email==''):
        #         return False
        #     else:
        #         return True
        return True

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
        
class ClientAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class DossierAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class ArticleAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class PlaceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class EmploiAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class EndettementAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class CompteEndettementAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True

class PretEndettementAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
        
# societe_site.register(User,Administrator)
societe_site.register(User, SetSocieteUserPermission)
societe_site.register(Client,ClientAdmin)
societe_site.register(Dossier,DossierAdmin)
societe_site.register(Article, ArticleAdmin)
societe_site.register(Societe,SetSocietePermission)
societe_site.register(Place,PlaceAdmin)
societe_site.register(Emploi, EmploiAdmin)
societe_site.register(Endettement,EndettementAdmin)
societe_site.register(CompteEndettement,CompteEndettementAdmin)
# societe_site.register(PretEndettement,PretEndettementAdmin)