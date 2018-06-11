from django.db import models
from django.template.defaultfilters import slugify

class Pagina(models.Model):
	titulo = models.CharField(max_length=100,help_text='El titulo de la pagina web')
	slug = models.SlugField(unique=True,max_length=120)
	categoria = models.ForeignKey('Categoria',blank=True,null=True)
	descripcion = models.CharField(max_length=150,help_text='La descripcion que se vera en la pagina para el buscador')
	activo = models.BooleanField(default=True)	
	estilo = models.CharField(max_length=100,blank=True)
	contenido = models.TextField(blank=True)

	def __unicode__(self):
		return self.slug

class Categoria(models.Model):
	titulo = models.CharField(max_length=100,help_text='Titulo de Categoria')
	slug = models.SlugField(unique=True,max_length=120)	

class Bloque(models.Model):
	titulo = models.CharField(max_length=100,blank=True,help_text='El titulo del bloque')
	page = models.ForeignKey(Pagina,blank=True,null=True,related_name='bloques')
	seccion = models.CharField(max_length=100,blank=True,help_text='El id donde se colocara')	
	estilo = models.CharField(max_length=100,blank=True)
	contenido = models.TextField(blank=True)
	template = models.CharField(max_length=100,blank=True,null=True)
	activo = models.BooleanField(default=True)


	def __unicode__(self):
		return "%s de %s " %(self.titulo,self.page)

class Carrusel(models.Model):
	TIPO = (
		('imagenes','Imagenes'),
		('productos','Productos'),
	)
	titulo = models.CharField(max_length=100,blank=True)
	page = models.ForeignKey(Pagina,blank=True,null=True,related_name='carruseles')	
	seccion = models.CharField(max_length=100,blank=True,help_text='El id donde se colocara')
	estilo = models.CharField(max_length=100,blank=True)	
	activo = models.BooleanField(default=True)
	template = models.CharField(max_length=100,blank=True,null=True)
	tipo = models.CharField(max_length=100,choices=TIPO)
	num_mostrar = models.PositiveIntegerField(default=1)
	navegacion = models.BooleanField(default=True)
	items = models.PositiveIntegerField(default=1)

class ImageCarrusel(models.Model):
	titulo = models.CharField(max_length=100,blank=True,help_text='Titulo que tendra la imagen en el Alt')
	estilo = models.CharField(max_length=100,blank=True)
	link = models.CharField(max_length=100,blank=True)
	carrusel = models.ForeignKey(Carrusel,blank=True,related_name='imagenes_carrusel')
	orden = models.PositiveIntegerField(default=0)
	imagen = models.ImageField(upload_to='bloque/carrusel')

class Menu(models.Model):
	titulo = models.CharField(max_length=100,blank=True)
	estilo = models.CharField(max_length=100,blank=True)
	template = models.CharField(max_length=100,blank=True)
	seccion = models.CharField(max_length=100,blank=True,help_text='El id donde se colocara')
	paginas = models.ManyToManyField(Pagina,blank=True,related_name='menus')
	activo = models.BooleanField(default=True)
	def __unicode__(self):
		return self.titulo

class LinkMenu(models.Model):
	nombre = models.CharField(max_length=100,blank=True)
	menu = models.ForeignKey(Menu, related_name='links')
	icono = models.CharField(max_length=100,blank=True)
	link = models.CharField(max_length=100,blank=True)
	estilo = models.CharField(max_length=100,blank=True)
	orden = models.PositiveIntegerField(default=0)

#Nuevas Forma de ralizar api

class HeroHome(models.Model):
	titulo = models.CharField(max_length=100,help_text='El titulo para identificar el hero')
	activo = models.BooleanField(default=True)
	imagen = models.ImageField(upload_to='hero')
	body = models.CharField(max_length=100,help_text='El texto que se mostrara',blank=True)
	subtitulo = models.CharField(max_length=100,blank=True)
	enlace = models.CharField(max_length=100,blank=True)
	estilo_body = models.CharField(max_length=100,help_text='Los estilos del texto que se mostrara',blank=True)

#class Dato(models.Model):
	#nombre = models.CharField(max_length=100,help_text='Nombre de La web')
	#titulo_seo = models.CharField(max_length=150,help_text='Titulo Seo')
	#descripcio_seo = models.TextField()
	#telefono = models.CharField(max_length=100,help_text='telefono fijo')
	#celular = models.CharField(max_length=100,help_text='celular')
	#locacion = models.CharField(max_length=100,help_text='Direccion fisica')
	#cant_min = models.CharField(max_length=100,help_text='Cantidad Minima para ofrecer envio Gratis')