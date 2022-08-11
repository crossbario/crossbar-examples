SEEDPHRASE="avocado style uncover thrive same grace crunch want essay reduce current edge"

crossbar_standalone:
	crossbar start --loglevel=info --config=config-standalone-trustroot.json

clients: client_good

client_good:
	python client.py --debug --url wss://localhost:8080 --realm realm1 --seedphrase $(SEEDPHRASE)

generate_certificates:
	python generate_certificates.py --debug \
		--seedphrase=$(SEEDPHRASE) \
		--realm=0x72b3486d38E9f49215b487CeAaDF27D6acf22115 \
		--outdir=./.crossbar/
