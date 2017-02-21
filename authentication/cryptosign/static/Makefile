crossbar:
	PYTHONPATH=../../../../crossbar python -m crossbar.controller.cli start

client_raw_key:
	python client_raw_key.py --realm devices --authid client01@example.com --key client01.key

client_raw_key_aio:
	python client_raw_key_aio.py --realm devices --authid client01@example.com --key client01.key

client_raw_key_debug:
	python client_raw_key.py --debug --realm devices --authid client01@example.com --key client01.key

client_ssh_agent:
	python client_ssh_agent.py --pubkey ~/.ssh/id_ed25519.pub
#	python client_ssh_agent.py --realm devices --authid client02@example.com --pubkey ~/.ssh/id_ed25519.pub
