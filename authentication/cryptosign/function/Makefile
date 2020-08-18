crossbar:
	crossbar start --loglevel=info

clients: client_good client_bad

client_good:
	python client.py --key .keys/client01.key

client_bad:
	python client.py --key .keys/client01-bad.key
