# mon_app/serializers.py
from rest_framework import serializers

from .models import Actualite

class ActualiteSerializer(serilizers.ModelSerializer):
    class Meta:


