crossbar:
	rm -f .crossbar/cookies.dat
	MYSECRET="secret123" crossbar edge start

crossbar_rtrpxy:
	rm -f .crossbar/cookies.dat
	MYSECRET="secret123" crossbar start --config=config-rtrpxy.json
#	MYSECRET="secret123" crossbar edge start --config=config-rtrpxy.json

clients: client_good client_bad

client_good:
	MYSECRET="secret123" python client.py client1

client_bad:
	MYSECRET="wrongpassword" python client.py client1

test_derive_key_py:
	python -c "from autobahn.wamp.auth import derive_key; print(derive_key('secret123', 'salt123', 100, 16).decode() == 'DpHHRlQ6UNULJlP9J8WkPw==')"
