crossbar:
	crossbar start

clients: client_tx_good client_tx_bad

client_good:
	python client.py --realm realm1 --authid foobar@example.com --password secret123

client_bad:
	python client.py --realm realm1 --authid foobar@example.com --password wrongpassword

client_tx_good:
	python client_tx.py --realm realm1 --authid foobar@example.com --password secret123

client_tx_bad:
	python client_tx.py --realm realm1 --authid foobar@example.com --password wrongpassword
