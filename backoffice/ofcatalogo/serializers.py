from rest_framework import serializers
from .models import *
from inventario.models import Inventario

class CatalogoProductoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Producto
		fields = ('__all__')

class InsumoSerializer(serializers.ModelSerializer):
	stock = serializers.SerializerMethodField()
	class Meta:
		model = Insumo
		fields = ('id','nombre','imagen','ancho','stock_alert','tipo','stock','unidad')

	def get_stock(self,obj):
		stock_num = 0
		stock = Inventario.objects.filter(insumo=obj.id).order_by('-fecha')
		if stock:
			for s in stock:
				stock_num = stock_num + s.aumento - s.consumo
		return stock_num