crossbar:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start

crossbar_debug:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug

wstest:
	~/wstest/bin/wstest -m fuzzingclient

wsperf:
	~/wsperf ws://127.0.0.1:9001 1 200000 1000 2000 results.json
