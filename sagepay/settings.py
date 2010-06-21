
ACCEPTED_CARD_TYPES = (
	('AMEX', 'American Express'),
	('DC', 'Discover Card'),
	('DELTA', 'Delta'),
	('JCB', 'JCB'),
	('MAESTRO', 'Maestro'),
	('MC', 'Mastercard'),
	('SOLO', 'Solo'),
	('VISA', 'Visa'),
	#('UKE', ''), # Special card type for "A Debit card for processing all currencies"
)

MODE_SIM = 'sim'
MODE_TEST = 'test'
MODE_LIVE = 'live'

ACCEPTED_MODES = (
	'sim', # Simulator
	'test', # Test (Requires SagePay account)
	'live', # Live (Requires SagePay account)
)

TRANSACTION_URLS = {
	'sim':'https://test.sagepay.com/Simulator/VSPDirectGateway.asp',
	'test':'https://test.sagepay.com/gateway/service/vspdirect-register.vsp',
	'live':'https://ukvps.protx.com/vspgateway/service/vspdirect-register.vsp'
}

AUTH_3D_SECURE_URLS = {
	'sim':'https://test.sagepay.com/Simulator/VSPDirectCallback.asp',
	'test':'https://test.sagepay.com/gateway/service/direct3dcallback.vsp',
	'live':'https://live.sagepay.com/gateway/service/direct3dcallback.vsp'
}

REFUND_URLS = {
	'sim':'https://test.sagepay.com/Simulator/VSPDirectGateway?service=refund',
	'test':'https://test.sagepay.com/gateway/service/refund.vsp',
	'live':'https://live.sagepay.com/gateway/service/refund.vsp'
}