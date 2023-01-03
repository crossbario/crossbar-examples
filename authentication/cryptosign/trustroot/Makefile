SEEDPHRASE="avocado style uncover thrive same grace crunch want essay reduce current edge"
BAD_SEEDPHRASE="edge current reduce essay want crunch grace same thrive uncover style avocado"

crossbar_standalone:
	crossbar start --loglevel=info --config=config-standalone.json

crossbar_shared:
	crossbar start --loglevel=info --config=config-shared.json

clients: client_good client_bad

client_good:
	python client.py --debug --url wss://localhost:8080 --realm realm1 --channel_binding "tls-unique" --challenge --seedphrase $(SEEDPHRASE)

client_bad:
	python client.py --debug --url wss://localhost:8080 --realm realm1 --channel_binding "tls-unique" --challenge --seedphrase $(BAD_SEEDPHRASE)

generate_certificates:
	python generate_certificates.py --debug \
		--seedphrase=$(SEEDPHRASE) \
		--realm=0x72b3486d38E9f49215b487CeAaDF27D6acf22115 \
		--outdir=./.crossbar/

print_certificates:
	python print_certificates.py
