SEEDPHRASE="avocado style uncover thrive same grace crunch want essay reduce current edge"

crossbar_standalone:
	crossbar start --loglevel=info --config=config-standalone-trustroot.json

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

generate_certificates:
	python generate_certificates.py --debug \
		--seedphrase=$(SEEDPHRASE) \
		--realm=0x72b3486d38E9f49215b487CeAaDF27D6acf22115 \
		--outdir=./.crossbar/
