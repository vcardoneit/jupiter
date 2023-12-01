from rest_framework import serializers
from .models import prenotazioni


class prenotazioniSer(serializers.ModelSerializer):
    class Meta:
        model = prenotazioni
        fields = '__all__'
