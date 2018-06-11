from .models import *
from rest_framework import serializers

class FormCustomSerializer(serializers.ModelSerializer):
	class Meta:
		model = FormCustom
		fields = ('__all__')

class ImagenCustomSerializer(serializers.ModelSerializer):
	class Meta:
		model = ImagenCustom
		fields = ('__all__')