from __future__ import unicode_literals

from django.db import models
from catalogo.models import Producto
from django.contrib.auth.models import User as User
from django.db.models import Sum

# Create your models here.
class Comentario(models.Model):
	producto = models.ForeignKey(Producto,blank=True,null=True)
	usuario = models.ForeignKey(User, null=True,blank=True)
	verificado = models.BooleanField(default=False)
	valoracion = models.PositiveIntegerField(default=0)
	comentario = models.TextField(blank=True)
	email_invitado = models.CharField(max_length=100,blank=True,null=True)
	creado = models.DateTimeField(auto_now_add=True)
	full_name_invitado = models.CharField(max_length=100,blank=True)
	apellido_invitado = models.CharField(max_length=100,blank=True)
	activo = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if self.producto and len(self.comentario) > 30:
			if self.usuario or self.email_invitado:
				self.activo = True
		super(Comentario, self).save(*args, **kwargs)
		self.getRecomendacion()

	def getRecomendacion(self):
		valor = Comentario.objects.filter(producto=self.producto,activo=True).aggregate(total_valoracion=Sum('valoracion'))
		num = Comentario.objects.filter(producto=self.producto,activo=True).count()
		if num != 0:
			self.producto.recomendado = valor['total_valoracion'] * num
			self.producto.save()

class ComentarioImagen(models.Model):
	comentario = models.ForeignKey(Comentario,blank=True,null=True,related_name='fotos_comentario')
	foto = models.ImageField(upload_to='comentarios',blank=True,null=True,max_length=250)    