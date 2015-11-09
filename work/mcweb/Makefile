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

# test Crossbar.io JSON value path service
test_json:
	weighttp -n 5000000 -c 128 -t 8 -k http://10.0.1.3:8080/json
	wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json

# test Crossbar.io Twisted Web resource path service
test_resource:
	weighttp -n 5000000 -c 128 -t 8 -k http://10.0.1.3:8080/resource
	wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource

test:
	curl -s http://10.0.1.3:8080/resource?count=10000 | wc -c
