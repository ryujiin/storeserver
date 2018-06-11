from django.conf.urls import include, url
from views import *

urlpatterns = [
    url(r'^definir_pago/',definir_pago,name='definir_pago'),    
        #paypal
    url(r'^retorno_paypal/(?P<pedido>[-\w]+)/$',retorn_paypal,name='retorn_paypal'),    
    url(r'^cancel_paypal/(?P<pedido>[-\w]+)/$',cancel_paypal,name='cancel_paypal'),    
    url(r'^pago/paypal/', paypal_paymet,name = 'pago_paypal'),    
    url(r'^hardcode/get/paypal/', include('paypal.standard.ipn.urls')),
        #stripe
    url(r'^pago/stripe/$',stripe_paymet,name='pago_stripe'),
    url(r'^get_stripe_key/$',get_stripe_key,name='get_key'),    
        #mercado Pago
    url(r'^get_mercado_pago/', getForm_mercado_pago, name = 'mercado_pago'),
        #Contra Entrega
    url(r'^pago_contraentrega/',get_pago_contraentrega,name='pago_contraentrega'),    
]