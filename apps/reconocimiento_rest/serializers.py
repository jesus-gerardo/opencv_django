from rest_framework import serializers
from apps.reconocimiento import models

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.personas
        fields = ['id', 'registro', 'fecha_registro', 'foto']

class DatosPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.datos_personas
        fields = ['persona','temperatura', 'altura', 'peso', 'presion', 'fecha_registro']

class ImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.personas_imagenes
        fields = ['archivo', 'persona']