from django.db import models
from django.contrib.auth.models import User as User
from catalogo.models import Producto,ProductoVariacion
from ubigeo.models import *
from django.template.defaultfilters import slugify
from sorl.thumbnail import get_thumbnail

from django.utils.crypto import get_random_string

# Create your models here.
class Cliente(models.Model):
	GENEROS = (('Hombre','hombre'),('Mujer','mujer'),)
	usuario = models.OneToOneField(User,related_name='cliente', null=True,blank=True,unique=True)
	foto = models.ImageField(upload_to='perfiles',blank=True,null=True,max_length=250)
	genero = models.CharField(max_length=100,blank=True,null=True,choices=GENEROS)
	dni = models.CharField(max_length=10,blank=True,null=True)
	telefono = models.CharField(max_length=11,blank=True,null=True)
	year = models.IntegerField(default=0)
	mes = models.IntegerField(default=0)
	dia = models.IntegerField(default=0)

	def get_thum(self):
		if self.foto:
			img = get_thumbnail(self.foto, '100x100', crop='center', quality=99)
			return img.url
		else:
			return None


class CuponesCliente(models.Model):
	cliente =models.ForeignKey('Cliente')
	cupon = models.ForeignKey('CuponDescuento')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_uso = models.DateTimeField(blank=True,null=True)

class CuponDescuento(models.Model):
	nombre = models.CharField(max_length=100,help_text='El nombre del Cupon, Ejemplo: 2x1')
	slug = models.CharField(max_length=100,blank=True,unique=True)
	porcentaje_descuento = models.PositiveIntegerField(default=0)
	dias_duracion = models.PositiveIntegerField(default=0)
	activo = models.BooleanField(default=True)
	fecha_creacion =models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		super(CuponDescuento, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.nombre
    
class Direccion(models.Model):
	TIPO = (('envio','Direccion de envio'),('facturacion','Direccion de Facturacion'))
	default = models.BooleanField(default=False)
	nombre = models.CharField(max_length=100,blank=True,null=True)
	usuario = models.ForeignKey(User,related_name='direcciones', null=True,blank=True)
	tipo = models.CharField(max_length=100,blank=True,null=True,choices=TIPO)
	departamento = models.CharField(max_length=100,blank=True,null=True)
	provincia = models.CharField(max_length=100,blank=True,null=True)
	distrito = models.CharField(max_length=100,blank=True,null=True)
	direccion = models.CharField(max_length=100,blank=True,null=True)
	ubigeo = models.ForeignKey(Distrito,max_length=100,blank=True,null=True,related_name='direccion')
	referencia = models.CharField(max_length=200,blank=True,null=True)
	codigo_postal = models.CharField(max_length=20,blank=True,null=True)
	telefono = models.CharField(max_length=15,blank=True,null=True)

import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings

class Suscrito(models.Model):
	email = models.CharField(max_length=100,blank=True,null=True, unique=True)
	suscrito = models.BooleanField(default=True)
	usuario = models.BooleanField(default=True)
	cliente = models.ForeignKey(Cliente,blank=True,null=True)
	user = models.ForeignKey(User,blank=True,null=True)
	activo = models.BooleanField(default=True)
	cupon = models.ForeignKey(CuponDescuento,blank=True,null=True)

	def save(self, *args, **kwargs):
		random = get_random_string(length=6)
		nombre = "SUS%s-20" %(random.upper())
		slug = slugify(nombre)
		cupon = CuponDescuento(nombre=nombre,slug=slug,porcentaje_descuento=20)
		cupon.save()
		self.cupon = cupon
		super(Suscrito, self).save(*args, **kwargs)
		#enviar_email(self.email)

def enviar_email(email):
	sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
	data = {
		"personalizations": [{
			"to": [{
				"email": email
			}],
			"subject": "Bienvenido a la Familia Loviz DelCarpio.",
			"substitutions":{
			}
		}],
		"from": {
			"email": "admin@lovizdc.com"
			},
			"content": [{
				"type": "text/html",
				"value": "Hello, Email!"
		}],
		"template_id": "f8e2270c-2b38-40da-91f0-821e5293a1ab",
	}
	response = sg.client.mail.send.post(request_body=data)

class Favorito(models.Model):
	usuario = models.OneToOneField(User,null=True,blank=True,unique=True)
	producto = models.ForeignKey(Producto,blank=True,null=True,related_name='catalogo')
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "%s - %s" %(self.usuario,self.producto)

class Mayorista(models.Model):
	nombre = models.CharField(max_length=100)
	ruc = models.CharField(max_length=11,blank=True)
	direccion = models.CharField(max_length=40,blank=True)

	def __unicode__(self):
		return self.nombre