# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from backoffice.ofcatalogo.models import Insumo
from backoffice.inventario.models import Inventario
from backoffice.contabilidad.models import Egreso

# Create your models here.
class Compra(models.Model):
	insumo = models.ForeignKey(Insumo,blank=True)
	cantidad = models.PositiveIntegerField(default=0,blank=True)
	unidad = models.CharField(max_length=100, choices=settings.UNIDADES, blank=True)
	precio = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	fecha = models.DateField(auto_now=False,blank=True, null=True)
	inventario = models.ForeignKey(Inventario,blank=True, null=True)
	total = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,editable=False)

	def __unicode__(self):
		return "%s - %s S/.%s" %(self.insumo, self.cantidad,self.total)

	def save(self, *args, **kwargs):
		self.total = self.get_total()
		if not self.inventario:
			self.inventario = self.create_inventario()
		else:
			self.inventario.aumento = self.cantidad
			self.inventario.save()
		super(Compra, self).save(*args, **kwargs)
		# Guardar el egreso
		self.calcular_egreso()

	def create_inventario(self):
		if self.insumo.unidad != self.unidad:
			cantidad = self.cantidad * self.insumo.ratio
		else:
			cantidad = self.cantidad
		inventario = Inventario.objects.create(insumo=self.insumo,cantidad=cantidad,fecha=self.fecha)
		return inventario

	def get_total(self):
		return self.cantidad * self.precio

	def calcular_egreso(self):
		monto = 0
		egreso, created = Egreso.objects.get_or_create(fecha=self.fecha,tipo="compra")
		compras = Compra.objects.filter(fecha=self.fecha)
		for c in compras:
			monto = monto + c.total
		egreso.monto = monto
		egreso.save()
