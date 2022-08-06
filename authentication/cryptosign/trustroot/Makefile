SEEDPHRASE="avocado style uncover thrive same grace crunch want essay reduce current edge"

crossbar:
	crossbar start --loglevel=info

clients: client_tx_cnlbind_none client_tx_cnlbind_unique

client_tx_cnlbind_none:
	python client_tx.py --debug --url wss://localhost:8080 --realm realm1 \
		--seedphrase $(SEEDPHRASE) \
		--challenge \
		--trustroot 0x2F070c2f49a59159A0346396f1139203355ACA43

client_tx_cnlbind_unique:
	python client_tx.py --debug --url wss://localhost:8080 --realm realm1 \
		--seedphrase $(SEEDPHRASE) \
		--channel_binding="tls-unique" \
		--challenge \
		--trustroot 0x2F070c2f49a59159A0346396f1139203355ACA43

gen_root_ca_cert: gen_root_ca_cert_realm1 gen_root_ca_cert_realm2

gen_root_ca_cert_realm1:
	python gen_ca_cert.py --debug \
		--seedphrase=$(SEEDPHRASE) \
		--verifyingContract=0x163D58cE482560B7826b4612f40aa2A7d53310C4 \
		--realm=0x72b3486d38E9f49215b487CeAaDF27D6acf22115 \
		--keyno=0 \
		--certfile=./.crossbar/root_ca_cert_realm1.crt \

gen_root_ca_cert_realm2:
	python gen_ca_cert.py --debug \
		--seedphrase=$(SEEDPHRASE) \
		--verifyingContract=0x163D58cE482560B7826b4612f40aa2A7d53310C4 \
		--realm=0x52d66f36A7927cF9612e1b40bD6549d08E0513Ff \
		--keyno=1 \
		--certfile=./.crossbar/root_ca_cert_realm2.crt
