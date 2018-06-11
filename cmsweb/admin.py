from django.contrib import admin
from .models import *
# Register your models here.

class ImageCarruselInline(admin.TabularInline):
	model = ImageCarrusel

class CarruselAdmin(admin.ModelAdmin):
	inlines = [ImageCarruselInline,]

class MenuAdmin(admin.ModelAdmin):
	inlines = []

#admin.site.register(Pagina)
#admin.site.register(Bloque)
#admin.site.register(Carrusel,CarruselAdmin)
#admin.site.register(ImageCarrusel)
#admin.site.register(Menu,MenuAdmin)
admin.site.register(HeroHome)