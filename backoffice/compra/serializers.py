from rest_framework import serializers
from .models import *

class CompraSerializer(serializers.ModelSerializer):
	nombre_insumo = serializers.SerializerMethodField()
	class Meta:
		model = Compra
		fields = ('insumo','cantidad','unidad','fecha','total','nombre_insumo','precio')

	def get_nombre_insumo(self,obj):
		nombre = obj.insumo.nombre
		return nombre