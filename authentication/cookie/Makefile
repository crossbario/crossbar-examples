clean:
	rm -rf .crossbar/.cookies/
	rm -f .crossbar/cookies.dat

crossbar: clean
	MYSECRET="secret123" crossbar start

crossbar_database: clean
	MYSECRET="secret123" crossbar start --config=config-database.json

crossbar_rtrpxy_database: clean
	MYSECRET="secret123" crossbar edge start --config=config-rtrpxy-database.json

client:
	MYSECRET="secret123" python client.py client1
