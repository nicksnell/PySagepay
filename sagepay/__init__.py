"""SagePay Payment Gateway Interface"""

import urllib
import urllib2

from exceptions import *
from settings import *
from wrappers import *

__all__ = ('SagePayAPI',)

VERSION = '2.23'

class SagePayAPI(object):
	
	def __init__(self, vendor, mode=MODE_SIM):
		
		assert mode in ACCEPTED_MODES, u'The mode you have specified "%s" is not valid!' % mode
		
		self.vendor = vendor
		self.mode = mode
		
	def __unicode__(self):
		return u'<SagePay Interface for %s>' % self.vendor
		
	def register(self, transaction):
		"""Register a Payment with SagePay"""
		
		transaction = transaction.as_dict()
		transaction.update({
			'Vendor': self.vendor,
			'VPSProtocol': VERSION,
		})
		
		data = urllib.urlencode(transaction)
		request = urllib2.Request(TRANSACTION_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (TRANSACTION_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
			
		return response
		
	def authorize(self, md, pa_res):
		"""Authorize a 3D Secure Payment"""
		
		authorize = {
			'MD': md,
			'PaRes': pa_res,
		}
		
		data = urllib.urlencode(authorize)
		request = urllib2.Request(AUTH_3D_SECURE_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (AUTH_3D_SECURE_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
			
		return response
		
	def refund(self, refund):
		"""Make a Refund"""
		
		refund = refund.as_dict()
		refund.update({
			'Vendor': self.vendor,
			'VPSProtocol': VERSION,
			'TxType': 'REFUND',
		})
		
		data = urllib.urlencode(refund)
		request = urllib2.Request(REFUND_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (REFUND_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
			
		return response
