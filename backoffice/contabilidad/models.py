# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Ingreso(models.Model):
	fecha = models.DateTimeField(auto_now=False)
	monto = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	tipo = models.CharField(max_length=100,blank=True)
	nota = models.TextField(blank=True)

class Egreso(models.Model):
	fecha = models.DateTimeField(auto_now=False)
	monto = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	tipo = models.CharField(max_length=100,blank=True)
	nota = models.TextField(blank=True)

