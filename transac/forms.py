from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from main.models import Client,Place,Endettement,CompteEndettement,Emploi,PretEndettement
from main import models

class ClientForms(ModelForm):
    class Meta:
        model = Client
        fields = (
            'nom',
            'prenom',
            'phone_1',
            'phone_2',
            'date_naissance',
            'ville_naissance',
            # 'pays_naissance',
            'type_piece_id',
            'numero_piece_id',
            'how_connu',
            'email',
            'proprietaire',
            'parents',
            )
class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = (
            'adresse',
            'ville',
            'pays',
            'code_postal',           
            'anciennete',
            'loyer',
            # 'residence',
            # 'residence_actu',
            # 'ancienne_address',
            # 'ancienne_ville',
            # 'ancienne_code_postal',
            # 'ancienne_pays',
            # 'ancienne_anciennete',
            # 'ancienne_loyer',
            # 'ancienne_residence',
            # 'ancienne_residence_actu',
        )

class EmploiForm(ModelForm):
    class Meta:
        model = Emploi
        fields = (
            'denomination',
            'nom_societe',
            'adresse',
            'ville',
            'code_postal',
            'pays',
            'salaire_m',
            'anciennete',
            # 'poste_actu',
            # 'autre_revenu',
            # 'autre_rev_sum',
            # 'ancien_denomination',
            # 'ancien_nom_societe',
            # 'ancien_adresse',
            # 'ancien_ville',
            # 'ancien_code_postal',
            # 'ancien_pays',
            # 'ancien_salaire_m',
            # 'ancien_anciennete',
        )

class EndettementForm(ModelForm):
    class Meta:
        model = Endettement
        fields = (
            'phone_emploi',
            'nom_responsable',
            'saisi',
            'faillite',
            'charge',
            'charge_sum',
        )

class CompteEndettementForm(ModelForm):
    class Meta:
        models = CompteEndettement
        fields = (
            'endettement',
            'nom_banque',
            'type_compte',
            'compte',
            'nom_compte',  
        )

class PretEndettementForm(ModelForm):
    class Meta:
        models = PretEndettement
        fields = (
            'endettement',
            'nom_banque',
            'type_pret',
            'reste',
            'mensualite',
            # 'nom_banque_1',
            # 'type_pret_1',
            # 'reste_1',
            # 'mensualite_1',
            # 'nom_banque_2',
            # 'type_pret_2',
            # 'reste_2',
            # 'date',
        )