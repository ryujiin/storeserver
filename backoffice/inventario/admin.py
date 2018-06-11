# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

class InventarioAdmin(admin.ModelAdmin):
	list_display = ('id','producto','insumo','aumento','consumo')

# Register your models here.
admin.site.register(Inventario, InventarioAdmin)
