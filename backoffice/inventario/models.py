# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum

# Create your models here.
from backoffice.ofcatalogo.models import Producto, Insumo
# Create your models here.

class Inventario(models.Model):
	producto = models.ForeignKey(Producto, blank=True, null=True)
	insumo = models.ForeignKey(Insumo,blank=True, null=True)
	cantidad = models.IntegerField(default=0,blank=True,null=True)
	fecha = models.DateField(auto_now=False,blank=True)

	def __unicode__(self):
		nombre = ''
		if self.producto:
			tipo = 'Producto'
			nombre = self.producto
		if self.insumo:
			tipo = 'Insumo'
			nombre = self.insumo
		return "%s - %s ( %s )" %(tipo,nombre)

	def save(self, *args, **kwargs):
		super(Inventario, self).save(*args, **kwargs)

	def get_total(self):
		inventarios = Inventario.objects.filter(insumo=self.insumo,fecha__lte=self.fecha).aggregate(Sum('cantidad'))
		return inventarios['cantidad__sum']