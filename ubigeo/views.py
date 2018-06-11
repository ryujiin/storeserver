from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Departamento, Provincia, Distrito
from .serializers import (DepartamentoSerializer, ProvinciaSerializer,
    DistritoSerializer)

class DepartamentoListView(generics.ListAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('coddpto', 'nom_dpto')


class ProvinciaListView(generics.ListAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('coddpto', 'nom_dpto', 'nom_prov', 'idprov')


class DistritoListView(generics.ListAPIView):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('coddpto', 'nom_dpto', 'nom_prov', 'nom_dist', 'iddist')
