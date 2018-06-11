from rest_framework import serializers
from .models import *

from comentario.models import Comentario
from carro.models import Carro,LineaCarro
import decimal

class CatalogoSerializer(serializers.ModelSerializer):
	thum1 = serializers.SerializerMethodField()
	thum2 = serializers.SerializerMethodField()
	valor_producto = serializers.SerializerMethodField()
	precio_lista = serializers.SerializerMethodField()
	precio_venta = serializers.SerializerMethodField()
	categoria = serializers.SerializerMethodField()
	class Meta:
		model = Producto
		fields = ('id','nombre','full_name','slug',
					'texto_variacion','activo','thum1','thum2',
					'valor_producto','es_oferta','precio_lista','precio_venta','categorias','etiquetas','categoria')

	def get_thum1(self,obj):
		thum = obj.get_thum(0)
		return self.context['request'].build_absolute_uri(thum)

	def get_thum2(self,obj):
		thum = obj.get_thum(1)
		return self.context['request'].build_absolute_uri(thum)

	def get_valor_producto(self,obj):
		valoraciones = Comentario.objects.filter(producto=obj.id,activo=True)
		num = Comentario.objects.filter(producto=obj.id,activo=True).count()
		valor = 0.0
		valoracion = 0
		for varia in valoraciones:
			valor = valor+varia.valoracion
		if num!=0:
			valoracion = valor/num
		valoracion = decimal.Decimal(valoracion)
		return round(valoracion,1)

	def get_categoria(self,obj):
		cate = obj.categorias.filter(seccion="categoria")
		return cate[0].nombre

	def get_precio_lista(self,obj):
		precio = obj.get_precio_lista()
		precio ="%0.2f" %(precio)
		return precio

	def get_precio_venta(self,obj):
		precio= obj.get_precio_oferta_lista()
		precio ="%0.2f" %(precio)		
		return precio

class CategoriaSerializer(serializers.ModelSerializer):
	padre = serializers.CharField(read_only=True)
	link  = serializers.SerializerMethodField()
	imagen = serializers.SerializerMethodField()

	class Meta:
		model = Categoria
		fields = ('id','nombre','full_name','seccion','slug','descripcion','activo','imagen','padre','link','titulo_seo')

	def get_link(self,obj):
		link = '/catalogo/%s/' %obj.slug
		return link

	def get_imagen(self,obj):
		if obj.imagen:			
			return self.context['request'].build_absolute_uri(obj.imagen.url)
		else:
			return None


class ProductoVariacionSerializer(serializers.ModelSerializer):
	talla = serializers.CharField(read_only=True)
	precio_venta = serializers.SerializerMethodField('get_precio')
	precio = serializers.SerializerMethodField('get_precio_minorista')
	stock = serializers.SerializerMethodField()
	class Meta:
		model=ProductoVariacion
		fields =('id','talla','precio','oferta','precio_venta','stock')

	def get_precio(self,obj):
		precio = obj.get_precio()
		if precio:
			precio ="%0.2f" %(precio)
		else:
			precio = '%0.2f' %(obj.precio_minorista)
		return precio
		
	def get_precio_minorista(self,obj):
		precio = obj.precio_minorista
		precio ="%0.2f" %(precio)
		return precio

	def get_stock(self,obj):
		stock = obj.stock
		if stock == 0:
			stock = None
		return stock


class ParienteSerialiezer(serializers.ModelSerializer):
	thum = serializers.SerializerMethodField('get_img_thum')
	class Meta:
		model = Producto
		fields = ('id','nombre','full_name','thum','slug')

	def get_img_thum(self,obj):
		img = obj.get_thum(0)
		return self.context['request'].build_absolute_uri(img)

class ImgProductoSerializer(serializers.ModelSerializer):
	imagen = serializers.SerializerMethodField()
	imagen_medium = serializers.SerializerMethodField()
	imagen_thum = serializers.SerializerMethodField()
	class Meta:
		model = ProductoImagen
		fields =('id','imagen','imagen_medium','imagen_thum','orden','producto', 'foto')
	
	def get_imagen(self,obj):
		return self.context['request'].build_absolute_uri(obj.foto.url)

	def get_imagen_medium(self,obj):
		url = obj.get_thum_medium().url
		return self.context['request'].build_absolute_uri(url)

	def get_imagen_thum(self,obj):
		url = obj.get_thum().url
		return self.context['request'].build_absolute_uri(url)

class CaracteristicasSerializer(serializers.ModelSerializer):
	class Meta:
		model = CaracteristicasProducto		
		fields = ('__all__')

class ProductoSingleSereializer(serializers.ModelSerializer):
	caracteristicas = CaracteristicasSerializer(many=True)
	color= serializers.CharField(read_only=True)
	variaciones = ProductoVariacionSerializer(many=True)
	imagenes_producto = ImgProductoSerializer(many=True)
	thum = serializers.SerializerMethodField('get_thum_img')
	link = serializers.SerializerMethodField()
	relaciones = ParienteSerialiezer(many=True)

	precio = serializers.SerializerMethodField('get_precio_lista')
	precio_venta = serializers.SerializerMethodField('get_precio_descuento')
	precio_sort = serializers.SerializerMethodField()

	valoracion = serializers.SerializerMethodField()
	sort_valoracion = serializers.SerializerMethodField('get_valor_producto')
	num_comentarios=serializers.SerializerMethodField()
	categorias = CategoriaSerializer(many=True)

	nuevo = serializers.SerializerMethodField()

	class Meta:
		model = Producto
		fields = ('id','nombre','full_name','color','slug','activo','descripcion','thum','link',
				'precio','precio_venta','nuevo','texto_variacion',
				'imagenes_producto','variaciones','relaciones','video','valoracion','num_comentarios',
				'categorias','precio_sort','sort_valoracion','es_oferta','sku','caracteristicas')

	def get_nuevo(self,obj):
		nuevo = obj.guardar_novedad()
		return nuevo

	def get_precio_sort(self,obj):
		precio= obj.get_precio_oferta_lista()
		return precio
		
	def get_thum_img(self,obj):
		thum = obj.get_thum(0)
		return self.context['request'].build_absolute_uri(thum)

	def get_link(self,obj):
		link = '/producto/%s/' %obj.slug
		return link

	def get_precio_lista(self,obj):
		precio = obj.get_precio_lista()
		precio ="%0.2f" %(precio)
		return precio

	def get_precio_descuento(self,obj):
		precio= obj.get_precio_oferta_lista()
		precio ="%0.2f" %(precio)		
		return precio

	def get_valor_producto(self,obj):
		valoraciones = Comentario.objects.filter(producto=obj.id,activo=True)
		num = Comentario.objects.filter(producto=obj.id,activo=True).count()
		valor = 0.0
		valoracion = 0
		for varia in valoraciones:
			valor = valor+varia.valoracion
		if num!=0:
			valoracion = valor/num
		return valoracion

	def get_valoracion(self,obj):
		valoracion = self.get_valor_producto(obj)
		valoracion ="%0.1f" %(valoracion)		
		return valoracion

	def get_num_comentarios(self,obj):
		return Comentario.objects.filter(producto=obj.id,activo=True).count()

class TallasDisponiblesSerializer(serializers.ModelSerializer):
	talla = serializers.CharField(read_only=True)
	class Meta:
		model = ProductoVariacion
		fields = ('talla','stock')

class EtiquetaSerializer(serializers.ModelSerializer):
	num_productos = serializers.SerializerMethodField()
	class Meta:
		model = Etiqueta
		fields = ('id','nombre','num_productos')

	def get_num_productos(self,obj):
		return obj.numProductos()

class ProductoListaSerializers(serializers.ModelSerializer):
	color = serializers.CharField(read_only=True)
	thum = serializers.SerializerMethodField('get_thum_img')
	precio = serializers.SerializerMethodField('get_precio_lista')
	precio_venta = serializers.SerializerMethodField('get_precio_descuento')
	valoracion = serializers.SerializerMethodField()
	tallas_disponibles = serializers.SerializerMethodField()
	link = serializers.SerializerMethodField()	

	class Meta:
		model = Producto
		fields = ('id','nombre','full_name','color','slug','link',
				'thum','en_oferta','precio','precio_venta','valoracion','tallas_disponibles')

	def get_thum_img(self,obj):
		thum = obj.get_thum()
		return self.context['request'].build_absolute_uri(thum)

	def get_link(self,obj):
		link = '/producto/%s/' %obj.slug
		return link

	def get_precio_lista(self,obj):
		precio = obj.get_precio_lista()
		precio ="%0.2f" %(precio)
		return precio

	def get_precio_descuento(self,obj):
		precio= obj.get_precio_oferta_lista()
		precio ="%0.2f" %(precio)		
		return precio

	def get_valoracion(self,obj):
		valoracion = self.get_valor_producto(obj)
		valoracion ="%0.1f" %(valoracion)		
		return valoracion

	def get_valor_producto(self,obj):
		valoraciones = Comentario.objects.filter(producto=obj.id,activo=True)
		num = Comentario.objects.filter(producto=obj.id,activo=True).count()
		valor = 0.0
		valoracion = 0
		for varia in valoraciones:
			valor = valor+varia.valoracion
		if num!=0:
			valoracion = valor/num
		return valoracion

	def get_tallas_disponibles(self,obj):
		tallas = obj.get_tallas_disponibles()
		serializer = TallasDisponiblesSerializer(instance=tallas, many=True)
		return serializer.data

class ProductoAdminSerializer(serializers.ModelSerializer):
	class Meta:
		model = Producto
		fields =('__all__')
		
#Serializer de busqueda
#from drf_haystack.serializers import HaystackSerializer
#from search_indexes import ProductoIndex

#class ProductoBusquedaSerializer(HaystackSerializer):
	#class Meta:
		#index_classes = [ProductoIndex]
		#fields = ["text", "nombre", "categorias", "autocomplete"]


#Serializador Oficina
class ProductoListaSerializer(serializers.ModelSerializer):
	thum = serializers.SerializerMethodField()
	class Meta:
		model = Producto
		fields = ('id','nombre','full_name','thum')

	def get_thum(self,obj):
		thum = obj.get_thum().url
		return thum

class ProductoSingleEditable(serializers.ModelSerializer):
	class Meta:
		model = Producto

class ProductoVariacionAdminSerializer(serializers.ModelSerializer):
	talla_nombre = serializers.SerializerMethodField()
	class Meta:
		model = ProductoVariacion
		fields = ('__all__')

	def get_talla_nombre(self,obj):
		return obj.talla.nombre