from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models.expressions import Exists
from main.models import User,Societe
# Register your models here.

class Administrator(UserAdmin):
    list_display        = ('username','email','societe','last_login','is_admin')
    search_fields       = ('email', 'username')
    readonly_fields     = ('id','date_joined','last_login','updated_at')
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

    def get_queryset(self,request):
        User = get_user_model()
        users = User.objects.filter(is_staff = True)    
        return users 

    
    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        form.base_fields['username'].initial = 'default'

        if  is_superuser:    
            disabled_fields |= {
                'is_superadmin',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
   
class SocieteAdmin(admin.ModelAdmin):
    list_display        = ('nom','localisation','date_created')
    search_fields       = ('nom','active')
    readonly_fields     = ('id','date_created')
    filter_horizontal   = ()
    list_filter         = ()
    ordering            = (['nom'])
    fieldsets           = ()

admin.site.register(User,Administrator)

admin.site.register(Societe,SocieteAdmin)