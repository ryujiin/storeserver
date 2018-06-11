from django.shortcuts import render, render_to_response
from rest_framework import viewsets
from .models import *
from .serializers import *

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class PaginaViewsets(viewsets.ReadOnlyModelViewSet):
	serializer_class = PaginaSerializer

	def get_queryset(self):
		slug = self.request.query_params.get('slug', None)
		queryset = Pagina.objects.filter(activo=True)
		if slug:
			queryset = queryset.filter(slug=slug)
		return queryset

class HeroHomeViewsets(viewsets.ReadOnlyModelViewSet):
	serializer_class = HeroHomeSerializer

	def get_queryset(self):
		queryset = HeroHome.objects.filter(activo=True)
		return queryset

#class DatoViewsets(viewsets.ReadOnlyModelViewSet):
	#serializer_class = DatoSerializer
#
	#def get_queryset(self):
		#queryset = Dato.objects.get(pk=1)

class HomeView(TemplateView):
	template_name = "index.html"

class VerificarView(TemplateView):
	template_name = "veri.html"

class CustomView(TemplateView):
	template_name = "custom.html"

class Verificar(TemplateView):
	template_name = "text.html"

from django.middleware import csrf
import json
from django.http import HttpResponse


def get_csrf_token(request):
	token = csrf.get_token(request)
	return HttpResponse(json.dumps(token), content_type="application/json")
