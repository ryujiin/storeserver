# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from catalogo.models import Producto as Product

# Create your models here.
class Producto(models.Model):
	nombre = models.CharField(max_length=120,blank=True,null=True)
	imagen = models.ImageField(upload_to='catalogo/producto', blank=True)
	modelo = models.ForeignKey('ModeloProducto', blank=True)
	ecommerce = models.ForeignKey(Product,blank=True,null=True)

	def __unicode__(self):
		return self.nombre

class Insumo(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)
	imagen = models.ImageField(upload_to='catalogo/insumo', blank=True)
	tipo = models.ForeignKey('TipoInsumo', blank=True)
	ancho = models.IntegerField(default=0)
	superficie = models.IntegerField(default=0)
	unidad = models.CharField(max_length=20, choices=settings.UNIDADES, blank=True)
	stock_alert = models.IntegerField(default=0)
	ratio = models.IntegerField(default=0)

	def __unicode__(self):
		return self.nombre	

class TipoInsumo(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return self.nombre

class ModeloProducto(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return self.nombre

class SeccionModelo(models.Model):
	modelo = models.ForeignKey(ModeloProducto,blank=True)
	nombre = models.CharField(max_length=100,blank=True)
	insumo = models.ForeignKey(Insumo, blank=True, null=True)