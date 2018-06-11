from django.utils import timezone

from haystack import indexes
from models import Producto

class ProductoIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	nombre = indexes.CharField(model_attr="full_name")
	categorias = indexes.CharField(model_attr="categorias")

	autocomplete = indexes.EdgeNgramField()

	def get_model(self):
		return Producto

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(
			actualizado__lte=timezone.now()
			)