all:
	@echo "Targets: client1, client2, router"

client1:
	env PYTHONPATH=../../autobahn-python python client1.py

client2:
	env PYTHONPATH=../../autobahn-python python client2.py

router:
	env PYTHONPATH=../../crossbar python -m crossbar.controller.cli start
