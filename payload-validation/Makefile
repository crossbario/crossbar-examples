default:
	@echo "Targets: crossbar, client"

clean:
	rm -rf ./__pycache__

crossbar:
	crossbar start

client:
	python client.py --realm realm1 --authid client1@example.com --key client1.key
