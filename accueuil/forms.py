from django import forms
from django.forms import fields
from main.models import Client, ClientAppel

class ClientRdv(forms.ModelForm):

    phone_1 = forms.CharField(
        label = 'Numéro client',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': '674048984'}
        )
    )   

    nom = forms.CharField(
        label = 'Nom',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'DOSSO'}
        )
    )   

    prenom = forms.CharField(
        label = 'Prénom',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': 'Hubert'}
        )
    )   

    phone_2 = forms.CharField(
        label = 'Téléphone',
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'placeholder': '986876869'}
        )
    )   

    HOW_CONU_CHOICES = (
       ('PRESSE','Presse'),
       ('TELE', 'Tele'),
       ('RADIO','Radio'),
       ('CONNAISANCE','Connaisance'),
       ('AUTRE','Autre'),
    )
    
    how_connu = forms.ChoiceField(
        label = 'Comment nous a t-il connu ?',
        choices=HOW_CONU_CHOICES,
        required = True,
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )


    # how_connu = forms.ChoiceField(
    #     label = 'Comment nous a t-il connu ?',
    #     choices=HOW_CONU_CHOICES,
    #     required = True,
    #     widget = forms.Select(
    #         attrs = {'class': 'form-control'}
    #     )
    # )    

    class Meta:
        model = Client
        fields = ('phone_1','nom', 'prenom','how_connu', 'phone_2', 'how_connu')
        labels={
            'phone_1': 'Numéro client', 
            'nom':'Nom',
            'prenom': 'Prénom',
            'phone_2': 'Téléphone',
            'how_connu': 'Comment nous a t-il connu ?'
        }
        
# from client appel, I will tke date dappel and date
# class ClientAppelForm(forms.ModelForm):
#     date_ap = forms.DateField(
#         label = "Date d'appel",
#         required = True,
#         widget = forms.TextInput(
#             attrs = {'class': 'form-control'}
#         )
#     )  

#     date = forms.CharField(
#         label = "date",
#         required = True,
#         widget = forms.TextInput(
#             attrs = {'class': 'form-control'}
#         )
#     )  

#     class Meta:
#         model = ClientAppel,
#         fields = ('date_ap','date')
#         labels={
#             'date_ap':"Date d'appel",
#             'date': "Heur d'appel"
#         }