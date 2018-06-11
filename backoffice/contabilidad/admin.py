# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *
# Register your models here.
class EgresoAdmin(admin.ModelAdmin):
	list_display = ('id', 'fecha', 'monto', 'tipo')

class IngresoAdmin(admin.ModelAdmin):
	list_display = ('id', 'fecha', 'monto', 'tipo')
	
# Register your models here.
admin.site.register(Egreso, EgresoAdmin)
admin.site.register(Ingreso, IngresoAdmin)