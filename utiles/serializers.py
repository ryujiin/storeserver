from rest_framework import serializers
from .models import *


class ColorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Color
		fields = ('__all__')

class TallaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Talla
		fields = ('__all__')

