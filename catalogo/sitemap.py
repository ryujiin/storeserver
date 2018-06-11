from django.contrib.sitemaps import Sitemap
from .models import Categoria,Producto
import datetime

class CategoriaSitemap(Sitemap):
	changefreq = "never"
	priority = 0.5

	def items(self):
		return Categoria.objects.all()
	
	def lastmod(self, obj):
		return datetime.datetime.now()

class ProductoSitemap(Sitemap):
	changefreq = "weekly"
	priority = 0.5

	def items(self):
		return Producto.objects.filter(activo=True)

	def lastmod(self,obj):
		return obj.actualizado