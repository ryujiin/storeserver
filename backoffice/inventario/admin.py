# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

class InventarioAdmin(admin.ModelAdmin):
	list_display = ('id','producto','insumo','cantidad','fecha','get_total_today')

	def get_total_today(self,obj):
		total = obj.get_total()
		return total

# Register your models here.
admin.site.register(Inventario, InventarioAdmin)
