from django.db import models
from django.db.models import fields
from rest_framework import serializers
from main.models import Dossier, Facture

class DossierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dossier
        fields = '__all__'
        depth = 2


class FactureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Facture,
        fields = ('somme')
