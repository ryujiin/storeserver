# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from cliente.models import Mayorista
from cliente.models import Cliente
from backoffice.ofcatalogo.models import Producto
from utiles.models import Serie
from backoffice.cuenta.models import Cuenta
from backoffice.contabilidad.models import Ingreso

# Create your models here.
class VentaMayorista(models.Model):
	mayorista = models.ForeignKey(Mayorista,blank=True,null=True)
	producto = models.ForeignKey(Producto,blank=True,null=True)
	serie = models.ForeignKey(Serie, blank=True, null=True)
	cantidad = models.PositiveIntegerField(default=0)
	unidad = models.CharField(choices=settings.UNIDADES,blank=True,max_length=30)
	fecha = models.DateField(auto_now=False)
	precio = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	total = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

	def save(self, *args, **kwargs):
		self.total = self.get_total()
		super(Venta, self).save(*args, **kwargs)
		self.addCuentaCliente()
		self.calcular_ingreso()

	def get_total(self):
		total = self.precio * self.cantidad
		return total

	def addCuentaCliente(self):
		total = 0
		cuenta, created = Cuenta.objects.get_or_create(cliente=self.cliente,fecha=self.fecha,accion="mas")
		ventas = Venta.objects.filter(tipo='mayorista',cliente=self.cliente,fecha=self.fecha)
		for v in ventas:
			total = v.total + total
		cuenta.total_dia = total
		cuenta.save()

	def calcular_ingreso(self):
		monto = 0
		ingreso, created = Ingreso.objects.get_or_create(fecha=self.fecha,tipo="venta")
		ventas = Venta.objects.filter(fecha=self.fecha)
		for v in ventas:
			monto = monto + v.total
		ingreso.monto = monto
		ingreso.save()
