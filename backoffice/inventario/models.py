# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from backoffice.ofcatalogo.models import Producto, Insumo
# Create your models here.

class Inventario(models.Model):
	producto = models.ForeignKey(Producto, blank=True, null=True)
	insumo = models.ForeignKey(Insumo,blank=True, null=True)
	aumento = models.PositiveIntegerField(default=0,blank=True,null=True)
	consumo = models.PositiveIntegerField(default=0,blank=True,null=True)
	fecha = models.DateField(auto_now=False,blank=True)
	total = models.PositiveIntegerField(default=0,blank=True,null=True)

	def __unicode__(self):
		nombre = ''
		if self.producto:
			tipo = 'Producto'
			nombre = self.producto
		if self.insumo:
			tipo = 'Insumo'
			nombre = self.insumo
		return "%s - %s ( %s )" %(tipo,nombre,self.total)

	def save(self, *args, **kwargs):
		super(Inventario, self).save(*args, **kwargs)