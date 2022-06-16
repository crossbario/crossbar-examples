default:
	@echo "Targets: crossbar, client"

clean:
	rm -rf ./__pycache__

crossbar_static:
	crossbar start --config=config-static.json

crossbar_dynamic:
	crossbar start --config=config-dynamic.json

client:
	python client.py --realm realm1 --authid client1@example.com --key client1.key
