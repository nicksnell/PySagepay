"""SagePay Settings"""

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

ABORT_URLS = {
	'sim': 'https://test.sagepay.com/Simulator/VSPServerGateway.asp?Service=VendorAbortTx',
	'test': 'https://test.sagepay.com/gateway/service/abort.vsp',
	'live': 'https://live.sagepay.com/gateway/service/abort.vsp',
}

AUTH_3D_SECURE_URLS = {
	'sim': 'https://test.sagepay.com/Simulator/VSPDirectCallback.asp',
	'test': 'https://test.sagepay.com/gateway/service/direct3dcallback.vsp',
	'live': 'https://live.sagepay.com/gateway/service/direct3dcallback.vsp',
}

REFUND_URLS = {
	'sim': 'https://test.sagepay.com/Simulator/VSPServerGateway.asp?Service=VendorRefundTx',
	'test': 'https://test.sagepay.com/gateway/service/refund.vsp',
	'live': 'https://live.sagepay.com/gateway/service/refund.vsp',
}

RELEASE_URLS = {
	'sim': 'https://test.sagepay.com/Simulator/VSPServerGateway.asp?Service=VendorReleaseTx',
	'test': 'https://test.sagepay.com/gateway/service/release.vsp',
	'live': 'https://live.sagepay.com/gateway/service/release.vsp',
}

REPEAT_URLS = {
	'sim': 'https://test.sagepay.com/Simulator/VSPServerGateway.asp?Service=VendorRepeatTx',
	'test': 'https://test.sagepay.com/gateway/service/repeat.vsp',
	'live': 'https://live.sagepay.com/gateway/service/repeat.vsp',
}

TRANSACTION_URLS = {
	'sim':'https://test.sagepay.com/Simulator/VSPDirectGateway.asp',
	'test':'https://test.sagepay.com/gateway/service/vspdirect-register.vsp',
	'live':'https://ukvps.protx.com/vspgateway/service/vspdirect-register.vsp',
}
