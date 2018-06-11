from rest_framework import serializers
from .models import *
from carro.models import Carro
from django.conf import settings

from django.utils.timesince import timesince


class PagoSerializer(serializers.ModelSerializer):
	metodo_pago = serializers.CharField(read_only=True)
	class Meta:
		model = Pago

class PedidoSerializer(serializers.ModelSerializer):
	numero_pedido = serializers.CharField(read_only=True)
	estado_pedido = serializers.CharField(read_only=True)
	user = serializers.CharField(read_only=True)
	gasto_envio = serializers.CharField(read_only=True)
	tipo_pago = serializers.SerializerMethodField()
	fecha_compra = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p",required=False, read_only=True)
	total = serializers.SerializerMethodField()
	estado = serializers.SerializerMethodField()
	time_ago = serializers.SerializerMethodField()
	num_estado = serializers.SerializerMethodField()
	class Meta:
		model = Pedido
		fields = ('id','numero_pedido','user',
					'gasto_envio','direccion_envio',
					'metodoenvio','fecha_compra','estado_pedido',
					'metodo_pago','telefono_pedido','pago_pedido','fecha_final','tipo_pago','total','estado','time_ago','num_estado')

	def get_estado(self,obj):
		return obj.get_estado_pedido_display()

	def get_time_ago(self,obj):
		time = timesince(obj.fecha_compra)
		return time

	def get_tipo_pago(self,obj):
		tipo = ''
		if obj.metodo_pago:
			tipo = obj.metodo_pago.titulo
		return tipo

	def get_total(self,obj):
		total = 0
		carros = Carro.objects.filter(pedido=obj.pk)
		for carro in carros:
			total = carro.total_carro()
		return '%0.2f' %(total)

	def get_num_estado(self,obj):
		if obj.estado_pedido == 'autenticado':
			return 1
		if obj.estado_pedido == 'metodo_envio':
			return 2
		if obj.estado_pedido == 'esperando_pago' or obj.estado_pedido == 'pagado':
			return 3
		return 0

class MetodoEnvioSerializer(serializers.ModelSerializer):
	class Meta:
		model = MetodoEnvio
		fields = ('__all__')

class MetodoPagoSerializer(serializers.ModelSerializer):
	class Meta:
		model = MetodoPago
		fields = ('__all__')