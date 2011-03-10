"""SagePay API Exceptions"""

__all__ = ('SagePayAPIError', 'SagePayTransactionError')

class SagePayAPIError(Exception):
	pass
	
class SagePayTransactionError(Exception):
	pass