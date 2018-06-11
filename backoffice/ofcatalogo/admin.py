# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

class SeccionModeloInline(admin.TabularInline):
	model = SeccionModelo

class ModeloProductoAdmin(admin.ModelAdmin):
	inlines = [SeccionModeloInline,]

# Register your models here.
admin.site.register(Producto)
admin.site.register(Insumo)
admin.site.register(TipoInsumo)
admin.site.register(ModeloProducto, ModeloProductoAdmin)
