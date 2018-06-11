# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

class CuentaAdmin(admin.ModelAdmin):
	list_display = ('id','mayorista','fecha','accion','total_dia','get_total_cuenta')
# Register your models here.
admin.site.register(Cuenta, CuentaAdmin)
