from django.db import models
from django.template.defaultfilters import slugify

from sorl.thumbnail import get_thumbnail
from django.contrib.auth.models import User as User
from utiles.models import Color,Talla

from datetime import datetime, timedelta, time
from django.utils import timezone

from django.conf import settings

from random import randint

# Create your models here.
class Producto(models.Model):
	nombre = models.CharField(max_length=120,blank=True,null=True)
	texto_variacion = models.CharField(max_length=100,blank=True)	
	sku = models.CharField(max_length=14,blank=True,null=True,editable=False)
	full_name = models.CharField(max_length=120, unique=True,blank=True,null=True,editable=False)
	slug = models.CharField(max_length=120,editable=False,unique=True)
	relaciones = models.ManyToManyField('self',blank=True, related_name='relaciones')
	categorias = models.ManyToManyField('Categoria',blank=True,related_name='categorias_producto')
	activo = models.BooleanField(default=True)
	descripcion = models.TextField(blank=True,null=True)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)
	video = models.CharField(max_length=120, blank=True,null=True)
	es_oferta = models.BooleanField(default=False)
	etiquetas = models.ManyToManyField('Etiqueta',blank=True,related_name='etiquetas')

	def __unicode__(self):
		return "%s - %s" %(self.nombre,self.texto_variacion)

	def save(self, *args, **kwargs):
		self.full_name = "%s (%s)" %(self.nombre,self.texto_variacion)
		if not self.slug:
			self.slug = slugify(self.full_name)
		if not self.sku:
			self.sku = self.generarSku()
		super(Producto, self).save(*args, **kwargs)

	def get_thum(self,orden):
		if not orden:
			orden = 0
		img = ProductoImagen.objects.filter(producto=self).order_by('pk')
		if img:
			img = img[orden]
			img = get_thumbnail(img.foto, '450x350', quality=80)
			return img.url
		else:
			return None

	def guardar_novedad(self):
		dia_no_nuevo = timezone.now()-timedelta(days=20)
		if dia_no_nuevo > self.creado:
			return False
		else:
			return True

	def get_en_oferta(self):
		variaciones = self.get_variaciones()
		if variaciones:
			return variaciones[0].oferta
		else:			
			return 0

	def get_variaciones(self):
		variaciones = ProductoVariacion.objects.filter(producto=self).order_by('-oferta')
		return variaciones

	def get_precio_lista(self):
		en_oferta = self.get_en_oferta()
		if en_oferta:
			variaciones=self.get_variaciones()
		else:
			variaciones = ProductoVariacion.objects.filter(producto=self).order_by('-precio_minorista')
		if variaciones:
			precio = variaciones[0].precio_minorista
		else:
			precio = 0
		if not precio:
			precio = 0
		return precio

	def get_tallas_disponibles(self):
		tallas = ProductoVariacion.objects.filter(producto=self,stock__gt=0)
		return tallas

	def get_precio_oferta_lista(self):
		en_oferta = self.get_en_oferta()
		if en_oferta:
			variaciones=self.get_variaciones()
			precio_oferta = variaciones[0].precio_oferta
			return precio_oferta
		else:
			precio = self.get_precio_lista()
			return precio

	def get_parientes(self):
		parientes = self.parientes.all()
		return parientes

	def get_num_estrellas(self):
		num_entrellas = Comentario.objects.filter(producto=self)
		return num_entrellas

	def get_absolute_url(self):
		return "/producto/%s/" % self.slug


	def generarSku(self):
		return randint(100000000000, 9999999999999)

class Categoria(models.Model):
	SECCIONES = (
		('genero','Genero'),
		('categoria','Categoria'),
		('estilo','Estilo'),
		('coleccion','Coleccion'),
	)
	nombre = models.CharField(max_length=120)
	full_name = models.CharField(max_length=255,db_index=True, editable=False)
	padre = models.ForeignKey('self',blank=True,null=True)
	seccion = models.CharField(max_length=100,choices=SECCIONES,blank=True,null=True)
	slug = models.SlugField(max_length=120,unique=True,editable=False)
	titulo_seo = models.CharField(max_length=100,blank=True,null=True)	
	descripcion = models.TextField(blank=True,null=True)
	activo = models.BooleanField(default=True)
	imagen = models.ImageField(upload_to='categorias',blank=True,null=True,max_length=250)

	def __unicode__(self):
		return self.slug

	def get_absolute_url(self):
		return "/catalogo/%s/" % self.slug

	def save(self, *args, **kwargs):
		if self.padre:
			self.full_name = "%s - %s" %(self.nombre, self.padre.full_name)
		else:
			self.full_name = self.nombre
		if not self.slug:
			self.slug = slugify(self.full_name)
		super(Categoria, self).save(*args, **kwargs)

class ProductoVariacion(models.Model):
	producto = models.ForeignKey(Producto,related_name='variaciones')
	talla = models.ForeignKey(Talla)
	precio_minorista = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	oferta = models.PositiveIntegerField(default=0)
	precio_oferta = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	stock = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return "%s - %s" %(self.producto,self.precio_minorista)

	def get_precio(self):
		if self.precio_oferta:
			precio = self.precio_oferta
		else:
			precio = self.precio_minorista
		return precio

	def save(self, *args, **kwargs):
		if self.precio_minorista < self.precio_oferta:
			self.precio_oferta = self.precio_minorista
		if self.precio_oferta and self.precio_oferta != self.precio_minorista:
			self.oferta = (self.precio_minorista-self.precio_oferta)*100/self.precio_minorista
		super(ProductoVariacion, self).save(*args, **kwargs)
		if self.oferta>0:
			self.producto.es_oferta = True
			self.producto.save()

def url_imagen_pr(self,filename):
	url = "productos/imagen/%s/%s" % (self.producto.pk, filename)
	return url

class ProductoImagen(models.Model):
	producto = models.ForeignKey(Producto,related_name="imagenes_producto")
	foto = models.ImageField(upload_to=url_imagen_pr)
	orden = models.PositiveIntegerField(default=0)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ["orden"]

	def save(self, *args, **kwargs):
		orden_anterior = ProductoImagen.objects.filter(producto=self.producto).order_by('-orden')
		if orden_anterior:
			self.orden=orden_anterior[0].orden+1
		else:
			self.orden=0
		super(ProductoImagen, self).save(*args, **kwargs)

	def get_thum_medium(self):
		img = get_thumbnail(self.foto, '740x600', quality=80)
		return img

	def get_thum(self):
		img = get_thumbnail(self.foto, '150x100', quality=80)
		return img

class Etiqueta(models.Model):
	nombre = models.CharField(max_length=100)

	def __unicode__(self):
		return self.nombre

	def numProductos(self):
		return Producto.objects.filter(etiquetas=self).count()

class CaracteristicasProducto(models.Model):
	producto = models.ForeignKey(Producto,blank=True, related_name='caracteristicas')
	nombre = models.CharField(max_length=100, blank=True)
	descripcion = models.CharField(max_length=180, blank=True)