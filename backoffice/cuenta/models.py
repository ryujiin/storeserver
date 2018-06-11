# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from cliente.models import Mayorista

# Create your models here.
class Cuenta(models.Model):
	ACCION =(('mas','Aumento'),('menos','Disminuye'))
	mayorista = models.ForeignKey(Mayorista,blank=True,null=True)
	fecha = models.DateField(auto_now=False)
	accion = models.CharField(max_length=10,choices=ACCION)
	total_dia = models.IntegerField(default=0)

	def get_total_cuenta(self):
		total = 0
		cuentas = Cuenta.objects.filter(cliente=self.mayorista)
		for c in cuentas:
			if c.accion == 'mas':
				total = total + c.total_dia
			if c.accion == 'menos':
				total = total - c.total_dia
		return total
