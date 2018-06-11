from django.conf.urls import include, url
from views import *

urlpatterns = [
	url(r'^$',CarritoViewsApi.as_view()),
	url(r'^(?P<pk>[0-9]+)/$',CarritoDetailViews.as_view()),
]