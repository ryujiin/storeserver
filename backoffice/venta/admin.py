# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import VentaMayorista

class VentaAdmin(admin.ModelAdmin):
	list_display = ('id', 'fecha', 'producto', 'cantidad', 'precio', 'total')

# Register your models here.
admin.site.register(VentaMayorista, VentaAdmin)
