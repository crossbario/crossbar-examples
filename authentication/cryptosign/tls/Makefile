default:
	@echo "Targets:"
	@echo ""
	@echo "   test              Run a TLS router and a TLS client component in a container"
	@echo "   test_shared       Run 2 non-TLS Web workers sharing a TCP listening port"
	@echo "   test_shared_tls   Run 2 TLS Web workers sharing a TCP listening port"

test:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start

test_shared:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config=config_shared.json

test_shared_tls:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config=config_shared_tls.json

crossbar:
	PYTHONPATH=../../../../crossbar python -m crossbar.controller.cli start

client_raw_key:
	python client_raw_key.py --url wss://localhost:8080 --realm devices --authid client01@example.com --key client01.key

client_raw_key_aio:
	python client_raw_key_aio.py --url wss://localhost:8080 --realm devices --authid client01@example.com --key client01.key

client_raw_key_debug:
	python client_raw_key.py --debug --realm devices --authid client01@example.com --key client01.key

client_ssh_agent:
	python client_ssh_agent.py --pubkey ~/.ssh/id_ed25519.pub
#	python client_ssh_agent.py --realm devices --authid client02@example.com --pubkey ~/.ssh/id_ed25519.pub
