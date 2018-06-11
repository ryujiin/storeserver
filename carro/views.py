
from django.shortcuts import render
from rest_framework import viewsets

from django.http import HttpResponse, Http404
from .serializers import CarroSerializer,LineaSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *

class CarritoViewsApi(APIView):
	
	def get_object(self):
		coockie_carro = self.request.GET.get('session')
		if self.request.user.is_authenticated():
			try:
				return Carro.objects.get(propietario=self.request.user,estado="Abierto")
			except Carro.DoesNotExist:
				carro = Carro(propietario=self.request.user,estado="Abierto")
				carro.save()
				return carro
		else:
			try:
				return Carro.objects.get(sesion_carro=coockie_carro,estado="Abierto")
			except Carro.DoesNotExist:
				raise Http404


	def get(self,request,format=None):
		carro = self.get_object()
		serializer = CarroSerializer(carro)
		return Response(serializer.data,status=status.HTTP_200_OK)
		
	def post(self, request, format=None):
		serializer = CarroSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class CarritoDetailViews(APIView):
	def get_object(self,pk):
		try:
			return Carro.objects.get(pk=pk,estado='Abierto')
		except Carro.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		carro = self.get_object(pk)
		if carro.propietario:
			#El carro esta protejido para q lo vea su propietario cuando tiene
			if carro.propietario.id == request.user.id:
				serializer = CarroSerializer(carro)
				return Response(serializer.data)
			else:
				return Response({'detail':'El carro no te pertenece'}, status=status.HTTP_400_BAD_REQUEST)
		else:			
			serializer = CarroSerializer(carro)
			return Response(serializer.data)

	def put(self, request, pk, format=None):
		carro = self.get_object(pk)		
		#if request.user.is_authenticated():		
		if carro.propietario:
			#El carro esta protejido para q lo vea su propietario cuando tiene
			if carro.propietario.id == request.user.id:
				serializer = CarroSerializer(carro,data=request.data)
				if serializer.is_valid():
					serializer.save()
					return Response (serializer.data)
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'detail':'El carro no te pertenece'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			serializer = CarroSerializer(carro,data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response (serializer.data)
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LineasViewsets(viewsets.ModelViewSet):
	queryset = LineaCarro.objects.filter(activo=True)
	serializer_class = LineaSerializer

	def list(self,request):
		carro = request.GET.get('carro')
		if carro =='':
			carro = 0
		queryset = LineaCarro.objects.filter(carro=carro,activo=True)
		serializer = LineaSerializer(queryset,many=True)
		return Response(serializer.data)

	def create(self,request):
		#perfecto = False
		#carro_session = request.data['sesion_carro']
		#carro = request.data['carro']
		#carro_server = Carro.objects.get(pk=carro)
		#if carro_server.propietario:
			#if self.request.user.is_authenticated():
				#if self.request.user == carro_server.propietario:
					#perfecto = True
		#elif carro_server.sesion_carro == carro_session:
			#perfecto = True
		serializer = LineaSerializer(data=request.data)		
		if serializer.is_valid():
			serializer.save()
			return Response (serializer.data)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CarroViewsets(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	queryset = Carro.objects.all()
	serializer_class = CarroSerializer

	def create(self,request):
		pass
