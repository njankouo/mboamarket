# mon_app/serializers.py
from rest_framework import serializers

from .models import Actualite,SousActualite,Institution, Baniere, Groupe_institution



class SousactualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousActualite
        fields = ['id', 'intitule', 'prix']

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id','nom','sigle']

class BaniereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baniere
        fields = ['id', 'nom', 'logo']

class GroupeInstitution(serializers.ModelSerializer):
    class Meta:
        model = Groupe_institution
        fields = ['id', 'nom']
class ActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actualite
        fields = ['photos', 'intitule', 'prix', 'description', 'institution']  # 'fields' au lieu de 'filed'