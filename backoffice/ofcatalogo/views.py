# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import *

from .serializers import *

# Create your views here.
class ProductoLista(viewsets.ModelViewSet):
	serializer_class = CatalogoProductoSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Producto.objects.all()
		return queryset

class InsumoLista(viewsets.ModelViewSet):
	serializer_class = InsumoSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Insumo.objects.all()
		return queryset