from django.db import models
from rest_framework import serializers
from main.models import Dossier

class DossierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dossier
        fields = '__all__'
        depth = 2