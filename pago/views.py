from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseBadRequest,Http404,HttpResponse
from carro.models import Carro
from utiles.models import TipoCambio
from pedido.models import Pago,MetodoPago,Pedido
from cliente.models import Direccion
import json
import stripe
import urllib2
import urllib
import urlparse

from datetime import datetime, timedelta, time

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
@csrf_exempt
def stripe_paymet(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	
	if request.method == 'POST':
		datos = json.loads(request.body)
		try:
			card_token = datos['stripeToken']
			carro_id = datos['carro']
		except KeyError:
			return HttpResponseBadRequest('stripeToken not set')
		currency = getattr(settings, 'SHOP_CURRENCY', 'usd')
		carro = Carro.objects.get(pk = carro_id)
		pedido = carro.pedido
		amount = carro.total_carro()
		amount = int(amount*100)
		if request.user.is_authenticated():
			propietario = request.user.email
		else:
			propietario = 'Invitado'
		description = '%s de %s' %(card_token,propietario)

		stripe_dict = {
			'amount': amount,
			'currency': currency,
			'card': card_token,
			'description': description,
		}
		try:
			stripe_result = stripe.Charge.create(**stripe_dict)
		except stripe.error.CardError, e:
			error = e
			return HttpResponse(json.dumps({'error',error}),
			content_type='application/json;charset=utf8')
		else:
			metodo = MetodoPago.objects.get(nombre='Stripe')            
			pago = Pago(cantidad = amount/100,
						id_pago=stripe_result['id'],
						descripcion=description,
						metodo_pago = metodo,
						transaccion = card_token)
			pago.save()
			#Grabar PEdido
			pedido.pago_pedido = pago
			pedido.metodo_pago = metodo
			pedido.save()
			carro.estado = carro.ENVIADA
			carro.save()
			request.session['pedido'] = pedido.numero_pedido
		return HttpResponse(json.dumps({'status': stripe_result['status'],'pedido': pedido.numero_pedido}),
			content_type='application/json;charset=utf8')
	else:
		raise Http404

def get_tipo_cambio():
	tipo_cambio = 0
	today = datetime.now().date()
	tipos_cambio = TipoCambio.objects.filter(fecha=today)
	for tipo in tipos_cambio:
		tipo_cambio = tipo.cambio
	if tipo_cambio==0:
		url = 'https://openexchangerates.org/api/latest.json?app_id=%s' %settings.API_CURRENCY
		req = urllib2.urlopen(url)
		content = req.read()
		data = json.loads(content)
		data = float(data["rates"]['PEN'])
		modelo = TipoCambio(cambio=data)
		modelo.save()
		tipo_cambio = data
	return tipo_cambio

def paypal_paymet(request):
	carro = request.GET.get('carro', False)
	pedido = request.GET.get('pedido', False)
	tipo_cambio = round(get_tipo_cambio(),2)
	if carro:
		try:
			carro = Carro.objects.get(pk = carro)
		except Carro, DoesNotExist:
			raise Http404('No hay pedido en el carro')
		total_carro = carro.total_carro()
		total_dolares = round(total_carro/tipo_cambio,2)
		
		paypal_dict = {
			"business": settings.PAYPAL_RECEIVER_EMAIL,
			"amount": total_dolares,
			"item_name": "Productos de LovizDC.com",
			"invoice": carro.pedido.numero_pedido,
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return_url": request.build_absolute_uri(reverse('retorn_paypal', kwargs={'pedido': pedido})),
			"cancel_return": "%s" %(settings.PAYPAL_URL_CANCEL_RETURN),
			"custom": "Comprando los mejores productos!",  # Custom command to correlate to some function later (optional)
			}
		form = PayPalPaymentsForm(initial=paypal_dict)
		context = {"form": form,'total_carro':total_carro,'tipo_cambio':tipo_cambio,'total_dolares':total_dolares}
		return render(request, "paypal.html", context)
	else:
		raise Http404("No Hay Pedido")

from django.shortcuts import redirect

@csrf_exempt
def retorn_paypal(request,pedido):
	metodo = MetodoPago.objects.get(nombre='Paypal')
	carro = Carro.objects.get(pedido__numero_pedido=pedido)
	pedido = carro.pedido

	carro.estado = carro.ENVIADA
	carro.save()

	pago = Pago(cantidad= carro.total_carro(),
				id_pago = pedido.numero_pedido,
				metodo_pago = metodo,
				descripcion = 'Pago por paypal',
				transaccion = '')
	pago.save()

	pedido.pago_pedido = pago
	pedido.save()

	url = "%s/%s" %(settings.PAYPAL_URL_FRONT_RETURN,pedido.numero_pedido)
	return HttpResponseRedirect(url)
	#return HttpResponse(json.dumps({'pedido':url}),content_type='application/json;charset=utf8')

def cancel_paypal(request,pedido):
	#Hacer algo
	url = "%s" %(settings.PAYPAL_URL_CANCEL_RETURN) 
	return HttpResponseRedirect(url)

def get_pago_contraentrega(request):
	if request.POST:
		metodo = MetodoPago.objects.get(nombre='Contra entrega')
		pedido = Pedido.objects.get(numero_pedido=request.POST.get('id_pago'))
		carro = Carro.objects.get(pedido=pedido.pk) 

		total = carro.total_carro()

		pago = Pago(cantidad= total,
				id_pago = pedido.numero_pedido,
				metodo_pago = metodo,
				descripcion = 'Pago contra entrega, esperando el pago cuando se envia',
				transaccion = request.POST['transaccion'])          
		pago.save()

		pedido.pago_pedido = pago
		pedido.metodo_pago = metodo
		pedido.save()
		
		carro.estado = carro.ENVIADA
		carro.save()
		
		request.session['pedido'] = pedido.numero_pedido;
		return HttpResponse(json.dumps({'status':'ok'}),content_type='application/json;charset=utf8')
	else:
		raise Http404("No Hay Pedido")

def get_stripe_key(request):
	return HttpResponse(json.dumps({'key':settings.STRIPE_PUBLIC_KEY}),content_type='application/json;charset=utf8')


from django.conf import settings

def definir_pago(request):
	valor = False
	if request.POST:
		if request.POST['direccion']:           
			try:
				direccion = Direccion.objects.get(pk=request.POST['direccion']);                        
				if direccion.ubigeo.parent.name == 'Lima':
					valor = True
			except Direccion.DoesNotExist:
				valor = False
	return HttpResponse(json.dumps({'valor':valor}),content_type='application/json;charset=utf8')


import mercadopago

def getForm_mercado_pago(request):
	mp = mercadopago.MP(settings.CLIENT_ID, settings.CLIENT_SECRET)

	if request.GET['carro']:
		try:
			carro = Carro.objects.get(pk=request.GET['carro'])
		except Carro.DoesNotExist:
			carro = False
		if carro:
			pedido = carro.pedido
			preference = {
				"items": [],
				'payer':{
					'name':"%s %s" %(carro.propietario.first_name,carro.propietario.last_name),
					'email':carro.propietario.email
				},
				'shipments':{
					'cost':float(pedido.metodoenvio.precio),
				},
				'back_urls':{
					'success': request.build_absolute_uri(reverse('retorn_mercado_pago', kwargs={'pedido': pedido.id})),
					'pending': "%s" %(settings.MERCADO_PAGO_FAIL),
					'failure': "%s" %(settings.MERCADO_PAGO_FAIL),
				},
				'notification_url':"%s/mercadopago_ipn/" %(settings.DOMAIN),
			}
			for linea in carro.lineas.all():
				item = {
					'title':linea.producto.full_name,
					'picture_url':linea.producto.get_thum(0),
					'quantity':linea.cantidad,
					'currency_id':"PEN",
					"unit_price":float(linea.get_precio())
				}
				preference['items'].append(item)
			

			preferenceResult = mp.create_preference(preference)

			return HttpResponse(json.dumps(preferenceResult, indent=4),content_type='application/json;charset=utf8')
		else:
			return HttpResponse(json.dumps({'error':'No Existe Carro'}, indent=4),content_type='application/json;charset=utf8')         
	else:
		return HttpResponse(json.dumps({'error':'Solicitud no Valida'}, indent=4),content_type='application/json;charset=utf8')

def retorn_mercado_pago(request, pedido):
	metodo = MetodoPago.objects.get(nombre='Mercado Pago')
	carro = Carro.objects.get(pedido__numero_pedido=pedido)
	pedido = carro.pedido

	carro.estado = carro.ENVIADA
	carro.save()

	pago = Pago(cantidad= carro.total_carro(),
				id_pago = pedido.numero_pedido,
				metodo_pago = metodo,
				descripcion = 'Pago por Mercado Pago',
				transaccion = '')
	pago.save()

	pedido.pago_pedido = pago
	pedido.save()

	url = "%s/%s" %(settings.PAYPAL_URL_FRONT_RETURN,pedido.numero_pedido)
	return HttpResponseRedirect(url)

def mercadopago_succes(request,pedido):

	carro = Carro.objects.get(pedido__numero_pedido=pedido)
	pago = Pago(cantidad = carro.total_carro(),
						id_pago='',
						descripcion='',
						metodo_pago = '',
						transaccion = '')
	pago.save()
	carro.estado = carro.ENVIADA
	carro.save()
	url = "%s/%s" %(settings.PAYPAL_URL_FRONT_RETURN,pedido)
	return HttpResponseRedirect(url)

def mercadopago_pending(request,pedido):
	url = "%s" %(settings.SITE_NAME)
	return HttpResponseRedirect(url)

def mercadopago_fail(request,pedido):
	url = "%s" %(settings.SITE_NAME)
	return HttpResponseRedirect(url)

def mercadopago_ipn(request):
	mp = mercadopago.MP(settings.CLIENT_ID, settings.CLIENT_SECRET)

	paymentInfo = mp.get_payment_info(request.GET.get('id'))

	print paymentInfo
	
	# Show payment information
	if paymentInfo["status"] == 200:
		return paymentInfo["response"]
	else:
		return None