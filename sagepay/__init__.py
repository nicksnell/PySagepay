"""SagePay Payment Gateway Interface"""

import urllib
import urllib2

from exceptions import *
from settings import *
from wrappers import *

__all__ = ('SagePayAPI',)

SAGEPAY_VERSION = '2.23'

class SagePayAPI(object):
	
	def __init__(self, vendor, mode=MODE_SIM):
		
		assert mode in ACCEPTED_MODES, u'The mode you have specified "%s" is not valid!' % mode
		
		self.vendor = vendor
		self.mode = mode
		
	def __unicode__(self):
		return u'<SagePay Interface for %s>' % self.vendor
	
	def _encode_arguments(self, params):
		"""UTF-8 encode the argument values - used primarily """
		return dict([k, v.encode('utf-8')] for k, v in params.items())
	
	def register(self, transaction):
		"""Register a Payment with SagePay"""
		
		transaction = transaction.as_dict()
		transaction.update({
			'Vendor': self.vendor,
			'VPSProtocol': SAGEPAY_VERSION,
		})
		
		data = urllib.urlencode(self._encode_arguments(transaction))
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
		
		data = urllib.urlencode(self._encode_arguments(authorize))
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
			'VPSProtocol': SAGEPAY_VERSION,
			'TxType': 'REFUND',
		})
		
		data = urllib.urlencode(self._encode_arguments(refund))
		request = urllib2.Request(REFUND_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (REFUND_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
			
		return response
