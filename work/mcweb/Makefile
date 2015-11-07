crossbar_w1:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w1.json

crossbar_w2:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w2.json

crossbar_w4:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w4.json

crossbar_w8:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w8.json

crossbar_w16:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w16.json

crossbar_w32:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w32.json

crossbar_w40:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w40.json

crossbar_w48:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w48.json

crossbar_debug_w1:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w1.json

crossbar_debug_w2:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w2.json

crossbar_debug_w4:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w4.json

crossbar_debug_w8:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w8.json

test:
	weighttp -n 1000000 -c 4000 -t 4 -k "http://127.0.0.1:8080/config"
