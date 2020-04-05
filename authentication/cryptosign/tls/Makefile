crossbar:
	crossbar start --loglevel=info

clients: client_tx_cnlbind_none client_tx_cnlbind_unique client_aio_cnlbind_none client_aio_cnlbind_unique

client_tx_cnlbind_none:
	python client_tx.py --url wss://localhost:8080 --key .keys/client01.key

client_tx_cnlbind_unique:
	python client_tx.py --url wss://localhost:8080 --key .keys/client01.key --channel_binding="tls-unique"

client_aio_cnlbind_none:
	@echo 'FIXME: client_aio_cnlbind_none'
	# python client_aio.py --url wss://localhost:8080 --key .keys/client01.key

client_aio_cnlbind_unique:
	@echo 'FIXME: client_aio_cnlbind_unique'
	# python client_aio.py --url wss://localhost:8080 --key .keys/client01.key --channel_binding="tls-unique"
