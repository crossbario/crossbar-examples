SEEDPHRASE="avocado style uncover thrive same grace crunch want essay reduce current edge"

crossbar:
	crossbar start --loglevel=info

clients: client_tx_cnlbind_none client_tx_cnlbind_unique client_aio_cnlbind_none client_aio_cnlbind_unique


client_tx_cnlbind_none:
	python client_tx.py --debug --url wss://localhost:8080 --seedphrase $(SEEDPHRASE) \
		--challenge \
		--trustroot 0x2F070c2f49a59159A0346396f1139203355ACA43

client_tx_cnlbind_unique:
	python client_tx.py --debug --url wss://localhost:8080 --seedphrase $(SEEDPHRASE) \
		--channel_binding="tls-unique" \
		--challenge \
		--trustroot 0x2F070c2f49a59159A0346396f1139203355ACA43


client_aio_cnlbind_none:
	@echo 'FIXME: client_aio_cnlbind_none'
	# python client_aio.py --url wss://localhost:8080 --seedphrase $(SEEDPHRASE)

client_aio_cnlbind_unique:
	@echo 'FIXME: client_aio_cnlbind_unique'
	# python client_aio.py --url wss://localhost:8080 --seedphrase $(SEEDPHRASE) --channel_binding="tls-unique"

sign:
	python trustroot.py \
		--trustroot-keyfile=./.trustroot/default.priv \
		--keyfile=./.delegate/default.pub \
		--certfile=./.delegate/default.crt
