"""Wrappers around SagePay operations"""

__all__ = ('SagePayResponse', 'SagePayTransaction', 'SagePayRefund', 'SagePayCard', 
			'SagePayBasket', 'SagePayItem')

class SagePayResponse(object):
	"""A wrapper around a HTTP response from SagePay. Operates like an immutable dictionary"""
	
	def __init__(self, raw_response=None):
		
		self._args = {}
		
		if raw_response:
			self.parse(raw_response)
	
	def __getitem__(self, key):
		"""Return a value from the response"""
		
		if not key in self._args:
			raise KeyError(u'The item "%s" does not exist in the response!')
			
		return self._args[key]
		
	def __setitem__(self, key, value):
		"""Not Implemented. Prevent items being set"""
		
		raise TypeError(u'SagePayResponse object does not support item assignment!')
		
	def parse(self, raw_response):
		"""Parse a HTTP response"""
		
		# Read through each line....
		for line in raw_response.split('\n'):
			# Check it isn't 'empty'
			if line.strip():
				try:
					name, value = line.split('=', 1)
				except Exception:
					raise RuntimeError(u'Malformed response! Line "%s"' % line)
				else:
					self._args[name.strip()] = value.strip()

class SagePayTransaction(object):
	"""The 'SagePayTransaction' class provides a data structure for registering and
	authorising (via 3D Secure) transactions."""
	
	ACCEPTED_OPTIONS = {
		'account_type': 'AccountType',
		'apply_3d_secure': 'Apply3DSecure',
		'apply_avs_cv2': 'ApplyAVSCV2',
		'basket': 'Basket',
		'client_ip_address': 'ClientIPAddress',
		'contact_number': 'ContactNumber',
		'contact_fax': 'ContactFax',
		'contact_email': 'ContactEmail',
		'customer_name': 'CustomerName',
		'gift_aid_payment': 'GiftAidPayment',
		
		'billing_firstname': 'BillingFirstnames',
		'billing_surname': 'BillingSurname',
		#'billing_address': 'BillingAddress',
		'billing_address1': 'BillingAddress1',
		'billing_city': 'BillingCity',
		'billing_country': 'BillingCountry',
		'billing_post_code': 'BillingPostCode',
		
		'delivery_firstname': 'DeliveryFirstnames',
		'delivery_surname': 'DeliverySurname',
		'delivery_address1': 'DeliveryAddress1',
		'delivery_city': 'DeliveryCity',
		'delivery_country': 'DeliveryCountry',
		'delivery_post_code': 'DeliveryPostCode',
	}
	
	ACCEPTED_TYPES = (
		'PAYMENT',
		'DEFERRED',
		'AUTHENTICATE',
	)
	
	ACCEPTED_ACCOUNT_TYPES = ('E','C','M')
	ACCEPTED_3D_SECURE_OPTIONS = ('0','1','2','3')
	ACCEPTED_AVS_CV2_OPTIONS = ('0','1','2','3')
	ACCEPTED_GIFT_AID_PAYMENT_OPTIONS = ('0','1')
	
	def __init__(self, _type, vendor_code, amount, currency, description, card, **options):
		
		# Sanity check
		assert _type in self.ACCEPTED_TYPES, u'Unrecognised transaction type "%s"' % _type
		assert isinstance(card, SagePayCard), u'Transaction card argument must be an instance of SagePayCard!'
		
		self.type = _type
		
		self.vendor_code = vendor_code
		self.amount = amount
		self.currency = currency
		self.description = description
		self.card = card
		
		for key, value in options.items():
			if key in self.ACCEPTED_OPTIONS:
				setattr(self, self.ACCEPTED_OPTIONS[key], value)
		
		# Sanity check the options
		if hasattr(self, 'basket'):
			assert isinstance(self.basket, SagePayBasket), u'Transaction basket argument ust be an instance of SagePayBasket!'
			
		if hasattr(self, 'gift_aid_payment'):
			assert self.gift_aid_payment in self.ACCEPTED_GIFT_AID_PAYMENT_OPTIONS, 'Invalid gift aid payment option!'
			
		if hasattr(self, 'apply_3d_secure'):
			assert self.apply_3d_secure in self.ACCEPTED_3D_SECURE_OPTIONS, 'Invalid 3d secure option!'
			
		if hasattr(self, 'apply_avs_cv2'):
			assert self.apply_3d_secure in self.ACCEPTED_AVS_CV2_OPTIONS, 'Invalid avs/cv2 option!'
			
		if hasattr(self, 'account_type'):
			assert self.account_type in self.ACCEPTED_ACCOUNT_TYPES, 'Invalid account type option!'
	
	def __getitem__(self, name):
		if hasattr(self, name):
			return self.__dict__[name]
		elif name in self.ACCEPTED_OPTIONS.values():
			return None
		else:
			raise AttributeError, u'SagePayTransaction has no attribute "%s"' % name
	
	def as_dict(self):
		"""Return a dictionary of the transaction"""
		
		data = {
			'TxType': self.type,
			'VendorTxCode': self.vendor_code,
			'Amount': self.amount,
			'Currency': self.currency,
			'Description': self.description,
		}
		
		data.update(self.card.as_dict())
		
		for key in self.ACCEPTED_OPTIONS.keys():
			actual_key = self.ACCEPTED_OPTIONS[key]
			if hasattr(self, actual_key):
				data[actual_key] = str(getattr(self, actual_key))
				
		return data
		
class SagePayRefund(object):
	"""The 'SagePayRefund' class provides a data structure for making a refund."""
	
	def __init__(self, vendor_tx_code, amount, currency, description, related_vps_id, related_vendor_tx_code, 
				related_security_code, related_authorisation_number):
				
		self.vendor_tx_code = vendor_tx_code
		self.amount = amount
		self.currency = currency
		self.description = description
		self.related_vps_id = related_vps_id
		self.related_vendor_tx_code = related_vendor_tx_code
		self.related_security_code = related_security_code
		self.related_authorisation_number = related_authorisation_number
		
	def as_dict(self):
		data = {
			'VendorTxCode': self.vendor_tx_code,
			'Amount': self.amount,
			'Currency': self.currency,
			'Description': self.description,
			'RelatedVPSTxId': self.related_vps_id,
			'RelatedVendorTxCode': self.related_vendor_tx_code,
			'RelatedSecurityKey': self.related_security_code,
			'RelatedTxAuthNo': self.related_authorisation_number,
		}
		
		return data
		
class SagePayCard(object):
	"""The 'VSPCard' class provides a data structure for payment cards."""
	
	ACCEPTED_OPTIONS = {
		'cv2': 'CV2',
		'issue_number': 'IssueNumber',
		'start_date': 'StartDate',
	}
	
	def __init__(self, holder, number, _type, expiry_date, **options):
		
		assert _type in [card[0] for card in ACCEPTED_CARD_TYPES], u'Unrecognised card type "%s"' % _type
		
		self.type = _type
		self.holder = holder
		self.number = number
		self.expiry_date = expiry_date
		
		for key, value in options.items():
			if key in self.ACCEPTED_OPTIONS:
				setattr(self, self.ACCEPTED_OPTIONS[key], value)
				
	def __getitem__(self, name):
		if hasattr(self, name):
			return self.__dict__[name]
		elif name in self.ACCEPTED_OPTIONS.keys():
			return None
		else:
			raise AttributeError, u'SagePayCard has no attribute "%s"' % name
			
	def as_dict(self):
		"""Returns a dictionary of the card details"""
		
		data = {
			'CardHolder': self.holder,
			'CardNumber': self.number,
			'CardType': self.type,
			'ExpiryDate': self.expiry_date,
		}
		
		for key in self.ACCEPTED_OPTIONS:
			actual_key = self.ACCEPTED_OPTIONS[key]
			if hasattr(self, actual_key):
				data[actual_key] = str(getattr(self, actual_key))
				
		return data
	
class SagePayBasket(object):
	""" """
	
	def __init__(self):
		self._lines = []
	
	def __unicode__(self):
		length = len(self._lines)
		
		return u'%s:%s' % (length, u':'.join([unicode(line) for line in self._lines]))
	
	def __str__(self):
		return str(self.__unicode__())
	
	def add(self, line):
		"""Add a line to the basket"""
		
		assert isinstance(line, SagePayItem), u'You can only add SagePayItem instances to your basket!'
		
		self._lines.append(line)
		
	def remove(self, line, strict=False):
		"""Remove a line from the basket, error if strict flag is enabled and line does not exist"""
		
		assert isinstance(line, SagePayItem), u'You can only remove SagePayItem instances from your basket!'
		
		if line in self._lines:
			self._lines.remove(line)
		else:
			if strict:
				raise ValueError, u'"%s" does not exist in Basket!'
				
	def has_line(self, line):
		"""Check if the basket contains a specific line"""
		
		assert isinstance(line, SagePayItem), u'Only SagePayItem instances can be in the Basket!'
		
		return line in self._lines
		
class SagePayItem(object):
	"""This class represents a Basket Item"""
	
	def __init__(self, description, quantity, value, tax, subtotal, total):
		self.description = description
		self.quantity = quantity
		self.value = value
		self.tax = tax
		self.subtotal = subtotal
		self.total = total
		
	def __unicode__(self):
		items = ('description', 'quantity', 'value', 'tax', 'subtotal', 'total')
		return u':'.join([self.escape(getattr(self, name)) for name in items])
		
	def __str__(self):
		return str(self.__unicode__())
	
	@staticmethod
	def escape(txt):
		
		# At the time of writing this Sage Pay provided no information on how you 
		# would escape the separator character ':'. It's possible that the
		# Sage Pay parser can't handle escaped separators.
		#
		# So at the moment I simply replace the sperator character with a
		# semi-colon ';'.
		
		return str(txt).replace(":",";")