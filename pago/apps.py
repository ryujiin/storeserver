from __future__ import unicode_literals

from django.apps import AppConfig
from paypal.standard.ipn.signals import valid_ipn_received
from signals import show_me_the_money

class PagoConfig(AppConfig):
	name = 'pago'

	def ready(self):
		valid_ipn_received.connect(show_me_the_money)
