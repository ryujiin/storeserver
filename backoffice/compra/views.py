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
		queryset = Compra.objects.all().order_by('-fecha')
		return queryset