from rest_framework import serializers
from .models import *

class ImagenCarruselSerializer(serializers.ModelSerializer):
	imagen = serializers.SerializerMethodField()
	class Meta:
		model = ImageCarrusel
		fields = ('id','titulo','estilo','orden','imagen','link')

	def get_imagen(self,obj):
		url = obj.imagen.url
		return url

class BloqueSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bloque
		fields = ('id','titulo','seccion','estilo','template')

class CarruselSerializer(serializers.ModelSerializer):
	imagenes_carrusel = ImagenCarruselSerializer(many=True)

	class Meta:
		model = Carrusel
		fields = ('id','titulo','seccion','estilo','template','imagenes_carrusel','num_mostrar','navegacion')


class PaginaSerializer(serializers.ModelSerializer):	
	carruseles = CarruselSerializer(many=True)
	class Meta:
		model = Pagina
		fields = ('id','titulo','slug','descripcion','activo','estilo','contenido','carruseles')


#Loviz 2.0
class HeroHomeSerializer(serializers.ModelSerializer):
	class Meta:
		model = HeroHome
		fields = ('__all__')

#class DatoSerializer(serializers.ModelSerializer):
	#class Meta:
		#model = Dato
		#fields = ('__all__')
