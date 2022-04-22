crossbar:
	MYSECRET="secret123" crossbar start

crossbar_database:
	MYSECRET="secret123" crossbar start --config=config-database.json

clients: client_good client_bad

client_good:
	MYSECRET="secret123" python client.py client1

client_bad:
	MYSECRET="wrongpassword" python client.py client1
