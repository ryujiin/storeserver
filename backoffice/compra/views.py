# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from .serializers import *

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.

class CompraApiViews(viewsets.ModelViewSet):
	serializer_class = CompraSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		insumo = self.request.query_params.get('insumo', None)
		dateInit = self.request.query_params.get('dateInit', None)
		dateEnd = self.request.query_params.get('dateEnd', None)

		queryset = Compra.objects.all().order_by('-fecha')

		if insumo:
			queryset = queryset.filter(insumo=insumo)[:1]
		if dateInit and dateEnd:
			queryset = queryset.filter(fecha__range=[dateInit, dateEnd])
		return queryset