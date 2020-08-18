crossbar:
	MYTICKET="secret123" crossbar start

clients: client_good client_bad

client_good:
	MYTICKET="secret123" python client.py client1

client_bad:
	MYTICKET="wrongpassword" python client.py client1
