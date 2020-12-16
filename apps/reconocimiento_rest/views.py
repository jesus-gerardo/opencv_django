from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from apps.reconocimiento import models
from . import serializers


class personasViewSet(viewsets.ModelViewSet):
    queryset = models.personas.objects.all()
    serializer_class = serializers.PersonaSerializer

class PersonasDatosViewSet(viewsets.ModelViewSet):
    queryset = models.datos_personas.objects.all()
    serializer_class = serializers.DatosPersonaSerializer

class personasImagenesViewSet(viewsets.ModelViewSet):
    queryset = models.personas_imagenes.objects.all()
    serializer_class = serializers.ImagenesSerializer

# Create your views here.
