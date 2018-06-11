# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from backoffice.ofcatalogo.models import Producto, Insumo
from django.conf import settings

# Create your models here.
class InsumoProducto(models.Model):
	producto = models.ForeignKey(Producto,blank=True)
	insumo = models.ForeignKey(Insumo,blank=True)
	seccion = models.ForeignKey('Seccion', blank=True)
	cantidad = models.PositiveIntegerField(default=0,blank=True)
	unidad = models.CharField(max_length=100, choices=settings.UNIDADES)

class Seccion(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)