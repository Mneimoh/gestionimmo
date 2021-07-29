from django import forms
from django.forms import fields
from main.models import ClientAppel

class AcceuilCreate(forms.ModelForm):
    class Meta:
        model = ClientAppel
        fields = '__all__'