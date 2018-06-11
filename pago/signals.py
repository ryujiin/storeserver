from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from pedido.models import Pedido,Pago,MetodoPago
from utiles.models import TipoCambio
from carro.models import Carro

from django.conf import settings

def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	
	if ipn_obj.payment_status == ST_PP_COMPLETED:

		pedido = Pedido.objects.get(numero_pedido=ipn_obj.invoice)
		carro = Carro.objects.get(pedido=pedido.pk)
		total = carro.total_carro()
		tipos_cambio = TipoCambio.objects.filter(fecha=today)
		metodo = MetodoPago.objects.get(nombre='Paypal')

		pago = Pago(cantidad=ipn_obj.mc_gross,
					id_pago=ipn_obj.auth_id,
					metodo_pago=metodo,
					transaccion=ipn_obj.invoice)
		if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
			pago.descripcion = 'Ocurrio un Error en el email de receptor'
			pago.save()
			return
		
		for tipo in tipos_cambio:
			tipo_cambio = tipo.cambio
		
		total_dolares = round(total/tipo_cambio,2)

		if ipn_obj.mc_gross == total_dolares and ipn.mc_currency == 'USD':
			pago.valido = True
			pago.descripcion = 'Todo Perfecto'
		else:
			pago.descripcion = 'El pago tiene datos incorrectos'

		pago.save()
		pedido.pago_pedido = pago
		pedido.metodo_pago = metodo
		pedido.save()

	#else:
		##...