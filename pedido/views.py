from django.shortcuts import render,render_to_response

from rest_framework import viewsets

from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from .models import * 
from carro.models import Carro,LineaCarro
from pedido.models import Pedido

class PedidoViewSet(viewsets.ModelViewSet):
	serializer_class = PedidoSerializer
	permission_classes = (IsAuthenticated,)
	http_method_names = ['get', 'put', 'head']

	def get_queryset(self):
		if self.request.user.is_authenticated:
			queryset = Pedido.objects.filter(user=self.request.user.pk).order_by('-pk').exclude(estado_pedido="fucionado")
		return queryset

class MetodoEnvioViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = MetodoEnvioSerializer

	def get_queryset(self):	
		pais = self.request.query_params.get('pais',None)
		
		queryset = MetodoEnvio.objects.filter(nombre=pais)
		return queryset
		#if self.request.user.is_authenticated():
			#try:
				#total = Carro.objects.get(propietario=self.request.user,estado="Abierto")
			#except Carro.DoesNotExist:
				#raise Http404
			#if int(total.total_carro())<50:
				##si es menor q 50
				#queryset = MetodoEnvio.objects.filter(grupo_metodo__nombre='Menores a 50')
			#else:
				#queryset = MetodoEnvio.objects.filter(grupo_metodo__nombre='Mayores a 50')
		#else:
			#queryset = MetodoEnvio.objects.filter(grupo=1)
		#return queryset.order_by('precio')

class MetodoPagoViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = MetodoPagoSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			queryset = MetodoPago.objects.all()
		return queryset

@csrf_exempt
def felicidades(request):
	if 'pedido' in request.session:		
		pedido = request.session['pedido'];
		pedido = get_object_or_404(Pedido,numero_pedido=pedido)
		carro = get_object_or_404(Carro,pedido=pedido)
		lineas = LineaCarro.objects.filter(carro=carro)
		for linea in lineas:
			producto = linea.producto
			producto.vendidos = producto.vendidos + linea.cantidad
			producto.save();
		request.session['pedido'] = ''
		return render_to_response('felicidades.html', {"pedido": pedido,'lineas':lineas})
	else:
		return redirect ('/')