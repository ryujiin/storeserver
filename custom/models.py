# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class FormCustom(models.Model):
	nombre = models.CharField(max_length=100,blank=True)
	email = models.CharField(max_length=100,blank=True,null=True)
	estilo = models.CharField(max_length=100,blank=True,null=True)

class ImagenCustom(models.Model):
	formulario = models.ForeignKey(FormCustom,blank=True,null=True)
	foto = models.ImageField(upload_to='custom',blank=True,null=True,max_length=250)