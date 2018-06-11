from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions, parsers, renderers, status

from .models import *
from .serializers import *

class CustomFormViewSet(viewsets.ModelViewSet):
	serializer_class = FormCustomSerializer
	queryset = FormCustom.objects.all()

class ImagenCustomViewSet(viewsets.ModelViewSet):
	serializer_class = ImagenCustomSerializer
	queryset = ImagenCustom.objects.all()