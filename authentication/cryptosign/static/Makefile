crossbar:
	crossbar start

clients: client_tx client_aio client_tx_noauthid client_aio_noauthid

client_tx:
	python client_tx.py --realm devices --authid client01@example.com --key .keys/client01.key

client_aio:
	python client_aio.py --realm devices --authid client01@example.com --key .keys/client01.key

client_tx_noauthid:
	python client_tx.py --realm devices --key .keys/client01.key

client_aio_noauthid:
	python client_aio.py --realm devices --key .keys/client01.key


client_ssh_agent:
	python client_ssh_agent.py --pubkey ~/.ssh/id_ed25519.pub
#	python client_ssh_agent.py --realm devices --authid client02@example.com --pubkey ~/.ssh/id_ed25519.pub
