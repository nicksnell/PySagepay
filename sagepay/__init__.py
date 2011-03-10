"""SagePay Payment Gateway Interface

Currently supports:
- Direct Payments (w/ 3D Secure)
- Refunds
- Deferred Payments with Release/Abort
"""

# Nick Snell <nick@orpo.co.uk>

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
	
	def abort(self, vps_id, vendor_tx_code, security_code, authorisation_number):
		"""Abort a deferred payment"""
		
		abort = {
			'Vendor': self.vendor,
			'VPSProtocol': SAGEPAY_VERSION,
			'TxType': 'ABORT',
			
			'VPSTxId': vps_id,
			'VendorTxCode': vendor_tx_code,
			'SecurityKey': security_code,
			'TxAuthNo': authorisation_number,
		}
		
		data = urllib.urlencode(self._encode_arguments(abort))
		request = urllib2.Request(ABORT_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (ABORT_URLS[self.mode], e))
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
	
	def paypal_capture(self, vps_id, ammount, accept=True):
		"""Authorize a PayPal Checkout"""
		
		# NOTE: It appears sometimes COMPLETE is not enabled on your SagePay account,
		# even when PayPal is enabled. You need to contact SagePay if this is the case.
		# Typically you will get an error:
		# 'INVALID 4006 : The TxType requested is not supported on this account'
		
		paypal_capture = {
			'TxType': 'COMPLETE',
			'VPSTxId': vps_id,
			'Amount': ammount,
			'Accept': 'YES' if accept else 'NO',
		}
		
		data = urllib.urlencode(self._encode_arguments(paypal_capture))
		request = urllib2.Request(PAYPAL_COMPLETE_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (PAYPAL_COMPLETE_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
		
		return response
	
	def refund(self, vendor_tx_code, amount, currency, description, related_vps_id, related_vendor_tx_code, 
				related_security_code, related_authorisation_number):
		"""Make a Refund"""
		
		refund = {
			'Vendor': self.vendor,
			'VPSProtocol': SAGEPAY_VERSION,
			'TxType': 'REFUND',
			
			'VendorTxCode': vendor_tx_code,
			'Amount': amount,
			'Currency': currency,
			'Description': description,
			'RelatedVPSTxId': related_vps_id,
			'RelatedVendorTxCode': related_vendor_tx_code,
			'RelatedSecurityKey': related_security_code,
			'RelatedTxAuthNo': related_authorisation_number,
		}
		
		data = urllib.urlencode(self._encode_arguments(refund))
		request = urllib2.Request(REFUND_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (REFUND_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
			
		return response
		
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
	
	def release(self, release_amount, vps_id, vendor_tx_code, security_code, authorisation_number):
		"""Release a payment that had previously be deferred"""
		
		release = {
			'Vendor': self.vendor,
			'VPSProtocol': SAGEPAY_VERSION,
			'TxType': 'RELEASE',
			
			'ReleaseAmount': release_amount,
			'VPSTxId': vps_id,
			'VendorTxCode': vendor_tx_code,
			'SecurityKey': security_code,
			'TxAuthNo': authorisation_number,
		}
		
		data = urllib.urlencode(self._encode_arguments(release))
		request = urllib2.Request(RELEASE_URLS[self.mode], data)
		
		try:
			response_page = urllib2.urlopen(request)
		except Exception, e:
			raise SagePayAPIError(u'Unable to contact "%s" because: %s' % (RELEASE_URLS[self.mode], e))
		else:
			response = SagePayResponse(response_page.read())
			
		return response
		