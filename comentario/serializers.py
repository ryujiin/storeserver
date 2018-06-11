from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User as User

class ComentarioImagenSerializer(serializers.ModelSerializer):
	class Meta:
		model = ComentarioImagen
		fields = ('__all__')

from django.utils.timesince import timesince

class ComentairoSerializer(serializers.ModelSerializer):
	creado = serializers.SerializerMethodField('get_tiempo_creado')
	nombre = serializers.SerializerMethodField('get_nombre_user')
	img_producto = serializers.SerializerMethodField('get_img')
	fotos_comentario = ComentarioImagenSerializer(many=True,read_only=True)
	thum_user = serializers.SerializerMethodField()
	nombre_producto = serializers.SerializerMethodField()
	slug_producto = serializers.SerializerMethodField()
	class Meta:
		model = Comentario
		fields = ('id','verificado',
			'email_invitado',
			'valoracion',
			'comentario',
			'creado',
			'producto',
			'usuario',
			'nombre',
			'img_producto',
			'fotos_comentario',
			'full_name_invitado',
			'apellido_invitado',
			'activo','thum_user','nombre_producto','slug_producto')

	def get_thum_user(self,obj):
		if obj.usuario:
			if obj.usuario.cliente.foto:
				return obj.usuario.cliente.get_thum()
			else:
				return None
		else:
			return None

	def get_slug_producto(self,obj):
		if obj.producto:
			return obj.producto.slug

	def get_nombre_producto(self,obj):
		if obj.producto:
			return obj.producto.full_name
		else:
			return None

	def get_tiempo_creado(self,obj):
		time = timesince(obj.creado)
		return time

	def get_nombre_user(self,obj):
		nombre = ''
		if obj.usuario:
			nombre = obj.usuario.username 
			if obj.usuario.first_name:
				nombre = "%s %s" %(obj.usuario.first_name,obj.usuario.last_name)
		else:
			nombre = "%s %s" %(obj.full_name_invitado,obj.apellido_invitado) 
		return nombre

	def get_img(self,obj):
		return obj.producto.get_thum(0)
