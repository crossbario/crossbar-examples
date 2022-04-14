crossbar:
	MYSECRET="secret123" crossbar start

clients: client_good client_bad

client_good:
	MYSECRET="secret123" python client.py client1

client_bad:
	MYSECRET="wrongpassword" python client.py client1
