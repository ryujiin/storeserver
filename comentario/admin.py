from django.contrib import admin
from .models import Comentario,ComentarioImagen
# Register your models here.
class ComentarioAdmin(admin.ModelAdmin):
	list_display = ('id','usuario','creado','producto','valoracion')


admin.site.register(Comentario,ComentarioAdmin)
admin.site.register(ComentarioImagen)
