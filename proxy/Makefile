CROSSBAR=crossbar

status:
	$(CROSSBAR) status


run_config1:
	$(CROSSBAR) start --config=config1.json

run_config2:
	$(CROSSBAR) start --config=config2.json

run_config3:
	$(CROSSBAR) start --config=config3.json

run_config4:
	$(CROSSBAR) start --config=config4.json

run_config5:
	$(CROSSBAR) start --config=config5.json


run_subscribe_ws_cbor:
	python client-subscribe.py websocket-cbor

run_subscribe_rs_cbor:
	python client-subscribe.py rawsocket-cbor

run_subscribe_ws_json:
	python client-subscribe.py websocket-json

run_subscribe_rs_json:
	python client-subscribe.py rawsocket-json


run_publish_ws_cbor:
	python client-publish.py websocket-cbor

run_publish_rs_cbor:
	python client-publish.py rawsocket-cbor

run_publish_ws_json:
	python client-publish.py websocket-json

run_publish_rs_json:
	python client-publish.py rawsocket-json


run_test_restbridge_call:
	curl -H "Content-Type: application/json" \
		-d '{"procedure": "com.example.add2", "args": [23, 666]}' \
		http://localhost:8443/call
	@echo ""
