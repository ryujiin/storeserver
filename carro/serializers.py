from rest_framework import serializers
from .models import *
from django.conf import settings
from catalogo.models import Producto
from pedido.models import MetodoEnvio,Pedido

class LineaSerializer(serializers.ModelSerializer):
	nombre = serializers.SerializerMethodField()
	full_name = serializers.SerializerMethodField()
	talla = serializers.SerializerMethodField()
	precio = serializers.SerializerMethodField()
	subtotal = serializers.SerializerMethodField()
	oferta = serializers.SerializerMethodField()
	thum = serializers.SerializerMethodField()
	genero = serializers.SerializerMethodField()
	class Meta:
		model = LineaCarro
		fields = ('id','carro','producto','variacion','thum','cantidad','nombre','talla','precio','subtotal','oferta','full_name','genero','activo')
	def get_nombre(self,obj):
		return obj.producto.nombre

	def get_full_name(self,obj):
		return obj.producto.full_name

	def get_talla(self,obj):
		return obj.variacion.talla.nombre

	def get_genero(self,obj):
		return obj.get_genero()

	def get_precio(self,obj):
		precio = obj.variacion.get_precio()
		return "%0.2f" %(precio)

	def get_subtotal(self,obj):
		subtotal = obj.get_subtotal()
		return "%0.2f" %(subtotal)

	def get_oferta(self,obj):
		return obj.variacion.oferta

	def get_thum(self,obj):
		thum = obj.producto.get_thum(0)
		return thum

class CarroSerializer(serializers.ModelSerializer):
	nombre_cupon = serializers.SerializerMethodField()
	desc = serializers.SerializerMethodField()
	rebaja = serializers.SerializerMethodField()
	lineas = LineaSerializer(many=True,read_only=True)
	pedido = serializers.SerializerMethodField()
	num_lineas = serializers.SerializerMethodField()
	total = serializers.SerializerMethodField()
	subtotal = serializers.SerializerMethodField()
	envio = serializers.SerializerMethodField()
	class Meta:
		model = Carro
		fields = ('id','propietario','estado','sesion_carro','num_lineas','total','subtotal','envio','pedido','lineas','cupon','nombre_cupon','desc','rebaja')

	def get_num_lineas(self,obj):
		lineas = obj.num_lineas()
		lineas = int(lineas)
		return lineas

	def get_total(self,obj):
		total =obj.total_carro()
		return '%0.2f' %(total)

	def get_subtotal(self,obj):
		subtotal = obj.subtotal_carro()
		return "%0.2f" %(subtotal)

	def get_envio(self,obj):
		envio =obj.envio_carro();
		return "%0.2f" %(envio)

	def get_pedido(self,obj):
		if obj.pedido:
			pedido = obj.pedido.pk
		else:
			pedido = None
		return pedido

	def get_rebaja(self,obj):
		return obj.get_rebaja()

	def get_nombre_cupon(self,obj):
		if obj.cupon:
			return obj.cupon.nombre
		else:
			return None

	def get_desc(self,obj):
		if obj.cupon:
			return obj.cupon.porcentaje_descuento
		return None
