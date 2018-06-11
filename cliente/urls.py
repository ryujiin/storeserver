from django.conf.urls import include, url
from views import *

urlpatterns = [
    url(r'^foto/$',cambiar_foto,name='foto_perfil'),    
    url(r'^perfil/$',PerfilViewSet.as_view(),name='prefil_user'),
    url(r'^sucribirse/$',SuscritoApiCreate.as_view(),name='suscrito'),
]