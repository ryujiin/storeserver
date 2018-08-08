"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.views.static import serve

from django.conf import settings

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from django.contrib.sitemaps.views import sitemap
from catalogo.sitemap import *



from django.contrib import admin
admin.autodiscover()

from catalogo.views import *
from cmsweb.views import *
from carro.views import LineasViewsets,CarroViewsets
from cliente.views import *
from comentario.views import ComentarioViewSet,ComentarioImagenViewSet
from pago.views import *
from custom.views import *
from pedido.views import PedidoViewSet,MetodoEnvioViewSet,MetodoPagoViewSet

#Backoffice
from backoffice.compra.views import CompraApiViews
from backoffice.ofcatalogo.views import InsumoLista,TipoInsumoLista

from utiles.views import ColorViewsets,TallasViewsets

router = DefaultRouter()
router.register(r'catalogo/productos', CatalogoViewsets,'productos')
router.register(r'catalogo/producto-single', ProductoSingleViewsets,'producto-single')

router.register(r'categoria', CategoriaViewsets,'categorias')
router.register(r'etiquetas', EtiquetaViewsets,'etiquetas')
router.register(r'carro/lineas', LineasViewsets,'lineas')
router.register(r'pedidos', PedidoViewSet,'pedidos')

router.register(r'cliente/cliente',ClienteEditViewSet,'cliente')
router.register(r'cliente/user',UserEditViewSet,'user')
router.register(r'cliente/direcciones',DireccionViewsets,'direcciones')
router.register(r'cliente/cupones',CuponViewSet,'direcciones')

router.register(r'custom/form',CustomFormViewSet,'custom_Form')
router.register(r'custom/imageForm',ImagenCustomViewSet,'custo_image')

router.register(r'metodos_envio',MetodoEnvioViewSet,'mentodos_envios')
router.register(r'metodos_pago',MetodoPagoViewSet,'mentodos_pago')
router.register(r'comentarios',ComentarioViewSet,'comentarios')
router.register(r'comentarioimgs',ComentarioImagenViewSet,'comentarios_imagenes')

router.register(r'cms/paginas', PaginaViewsets,'paginas')

router.register(r'colores',ColorViewsets,'colores')
router.register(r'tallas',TallasViewsets,'tallas')
#Loviz 2.0
router.register(r'cms/hero_home',HeroHomeViewsets,'Hero Home')

adminrouter = DefaultRouter()
adminrouter.register(r'conta/compra',CompraApiViews,'productos Admin')
adminrouter.register(r'catalogo/insumo',InsumoLista,'Insumos Admin')
adminrouter.register(r'catalogo/tipo_insumo',TipoInsumoLista,'Tipo Admin')

sitemaps ={
    'categoria': CategoriaSitemap,
    'productos':ProductoSitemap,
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^apiadmin/', include(adminrouter.urls)),
    url(r'^api/carro/', include('carro.urls')),
    url(r'^ubigeo/', include('ubigeo.urls')),
    #busqueda
    url(r'^search/$', SearchViewsets.as_view(), name="search"),
    #Usauario 
    url(r'^api/user/', include('cliente.urls')),        
    url(r'^ajax/crear/', nuevo_usuario, name='nuevo_usuario'),    
    url(r'^salir/$',salir,name='salir'),
    url(r'^login/$',ingresar,name='salir'),
    #url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^auth/', include('djoser.urls')),
    #Login
    #url('', include('social.apps.django_app.urls', namespace='social')),
    #pagos
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
    url(r'^return_mercado_pago/(?P<pedido>[-\w]+)/$', retorn_mercado_pago, name = 'retorn_mercado_pago'),
    url(r'^mercadopago_ipn/', mercadopago_ipn, name = 'mercado_pago_ipn'),
        #Contra Entrega
    url(r'^pago_contraentrega/',get_pago_contraentrega,name='pago_contraentrega'),
    #Web
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    name='django.contrib.sitemaps.views.sitemap')
]
if settings.DEBUG:
    #import debug_toolbar
    urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    #url(r'^debug/', include(debug_toolbar.urls)),
] + urlpatterns