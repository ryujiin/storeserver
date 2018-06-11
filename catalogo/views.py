from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import *
from django.db.models import Q

from .serializers import *

from datetime import datetime, timedelta, time

how_many_days = 20

class CatalogoViewsets(viewsets.ReadOnlyModelViewSet):
	serializer_class = CatalogoSerializer
	ordering_fields = ('precio_sort', 'num_comentarios')
	
	def get_queryset(self):
		if self.request.user.is_superuser:
			queryset = Producto.objects.all().order_by('-actualizado')
		else:
			queryset = Producto.objects.filter(activo=True).order_by('-actualizado')
		categoria = self.request.query_params.get('categoria', None)
		ordenado = self.request.query_params.get('ordenado', None)
		limite = self.request.query_params.get('limite',None)
		busqueda = self.request.query_params.get('busqueda',None)
		
		if categoria:
			if categoria == 'oferta':
				queryset = queryset.filter(es_oferta=True)
			elif categoria == 'novedades':
				queryset = queryset.filter(actualizado__gte=datetime.now()-timedelta(days=how_many_days))
			else:
				queryset = queryset.filter(categorias__slug=categoria)
		if busqueda:
			queryset = queryset.filter(Q(full_name__icontains=busqueda) | Q(descripcion__icontains=busqueda))
		if ordenado:
			queryset = queryset.order_by(ordenado)
		if limite:
			queryset = queryset[:limite]
		return queryset

class ProductoSingleViewsets(viewsets.ReadOnlyModelViewSet):
	serializer_class = ProductoSingleSereializer

	def get_queryset(self):
		if self.request.user.is_superuser:
			queryset = Producto.objects.all().order_by('-actualizado')
		else:
			queryset = Producto.objects.filter(activo=True).order_by('-actualizado')			
		slug = self.request.query_params.get('slug',None)
		ordenado = self.request.query_params.get('ordenado',None)
		if slug:
			queryset = queryset.filter(slug=slug)
		if ordenado:
			queryset = queryset.order_by(ordenado)
		return queryset

class EtiquetaViewsets(viewsets.ReadOnlyModelViewSet):
	serializer_class = EtiquetaSerializer

	def get_queryset(self):
		queryset = Etiqueta.objects.all()
		return queryset

class SearchViewsets(ListAPIView):
	serializer_class = CatalogoSerializer

	def get_queryset(self):
		queryset = Producto.objects.filter(activo=True).order_by('-actualizado')		
		query = self.request.query_params.get('query', None)
		if query:
			queryset = queryset.filter(Q(full_name__icontains=query) | Q(descripcion__icontains=query))
		return queryset

#from drf_haystack.viewsets import HaystackViewSet
##aun no se usa la busqueda mas adelante derrepente
#class ProductoBusquedaView(HaystackViewSet):
	#index_models = [Producto]
	#serializer_class = ProductoBusquedaSerializer


class CategoriaViewsets(viewsets.ReadOnlyModelViewSet):
	serializer_class = CategoriaSerializer
	queryset = Categoria.objects.all()

#Vistas para la oficina
class ProductosOficinaViewsets(viewsets.ModelViewSet):
	serializer_class = ProductoAdminSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Producto.objects.all().order_by('-pk')
		return queryset

class ProductoImageAdmin(viewsets.ModelViewSet):
	serializer_class = ImgProductoSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = ProductoImagen.objects.all().order_by('-pk')
		return queryset

class ProductoVariacionAdmin(viewsets.ModelViewSet):
	serializer_class = ProductoVariacionAdminSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = ProductoVariacion.objects.all()
		return queryset

class ProductoCaracteristica(viewsets.ModelViewSet):
	serializer_class = CaracteristicasSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = CaracteristicasProducto.objects.all()
		return queryset