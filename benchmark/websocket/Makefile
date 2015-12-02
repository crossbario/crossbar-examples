crossbar_w1:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w1.json

crossbar_w2:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w2.json

crossbar_w4:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w4.json

crossbar_w8:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --config config_w8.json

crossbar_debug_w1:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w1.json

crossbar_debug_w2:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w2.json

crossbar_debug_w4:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w4.json

crossbar_debug_w8:
	PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start --loglevel=debug --config config_w8.json

wstest:
	~/wstest/bin/wstest -m fuzzingclient

wsperf:
	~/wsperf ws://127.0.0.1:9001 1 10000 1000 2000 results.json

analyze:
	python ../../../wsperf/analyze.py results.json

test:
	~/wsperf ws://127.0.0.1:9001 8 500000 1000 2000 results_1.json
#	~/wsperf ws://127.0.0.1:9001 2 10000 1000 2000 results_2.json
#	~/wsperf ws://127.0.0.1:9001 4 10000 1000 2000 results_4.json
	python ../../../wsperf/analyze.py results_1.json
#	python ../../../wsperf/analyze.py results_2.json
#	python ../../../wsperf/analyze.py results_4.json
