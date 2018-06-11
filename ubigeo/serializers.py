from rest_framework import serializers

from .models import Departamento, Provincia, Distrito


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        exclude = []


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        exclude = []


class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        exclude = []
