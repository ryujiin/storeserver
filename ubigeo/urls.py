from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^regiones/$', views.DepartamentoListView.as_view(), name='ubigeo-region'),
    url(r'^provincias/$', views.ProvinciaListView.as_view(), name='ubigeo-provincia'),
    url(r'^distritos/$', views.DistritoListView.as_view(), name='ubigeo-distrito'),
]
