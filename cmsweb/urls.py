
from django.conf.urls import  include, url
from views import *
from pedido.views import felicidades

urlpatterns = [
	url(r'^$',HomeView.as_view() , name='index'),
	url(r'^get_token/',get_csrf_token , name='get_token'),
	#url(r'^sitemap\.xml$', 'cmsweb.views.sitemap',name='sitemap'),
	#url(r'^ingresar/$',TiendaView.as_view() , name='ingresar'),
	url(r'^catalogo/',HomeView.as_view() , name='catalogo'),
	url(r'^producto/',HomeView.as_view() , name='producto'),
	url(r'^carro/',HomeView.as_view() , name='carro'),
	url(r'^usuario/perfil/$',HomeView.as_view() , name='carro'),
	url(r'^procesar-compra/',HomeView.as_view() , name='procesar'),
	url(r'^0C32D5A4FC6AB8AEAB4A438740AF06C2.txt',Verificar.as_view() , name='procesar'),
	url(r'^p/',HomeView.as_view() , name='page_static'),
	url(r'^felicidades/$',felicidades , name='felicidades'),
	#url(r'^prueba_mercado/$',prueba_mercado_pago , name='mercado_pago'),
	#usuario reset
	url(r'^usuario/reset/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',HomeView.as_view() , name='password_reset_confirm'),
	#url(r'^custom/$',CustomView.as_view(), name='custom'),
]