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

run_config6:
	$(CROSSBAR) start --config=config6.json

run_config7:
	$(CROSSBAR) start --config=config7.json


run_subscribe_anon_ws_cbor:
	python client-subscribe.py anonymous-websocket-cbor

run_subscribe_anon_rs_cbor:
	python client-subscribe.py anonymous-rawsocket-cbor

run_subscribe_anon_ws_json:
	python client-subscribe.py anonymous-websocket-json

run_subscribe_anon_rs_json:
	python client-subscribe.py anonymous-rawsocket-json


run_publish_anon_ws_cbor:
	python client-publish.py anonymous-websocket-cbor

run_publish_anon_rs_cbor:
	python client-publish.py anonymous-rawsocket-cbor

run_publish_anon_ws_json:
	python client-publish.py anonymous-websocket-json

run_publish_anon_rs_json:
	python client-publish.py anonymous-rawsocket-json


run_subscribe_ticket_ws_cbor:
	python client-subscribe.py ticket-websocket-cbor

run_subscribe_ticket_rs_cbor:
	python client-subscribe.py ticket-rawsocket-cbor

run_subscribe_ticket_ws_json:
	python client-subscribe.py ticket-websocket-json

run_subscribe_ticket_rs_json:
	python client-subscribe.py ticket-rawsocket-json


run_publish_ticket_ws_cbor:
	python client-publish.py ticket-websocket-cbor

run_publish_ticket_rs_cbor:
	python client-publish.py ticket-rawsocket-cbor

run_publish_ticket_ws_json:
	python client-publish.py ticket-websocket-json

run_publish_ticket_rs_json:
	python client-publish.py ticket-rawsocket-json


run_test_restbridge_call:
	curl -H "Content-Type: application/json" \
		-d '{"procedure": "com.example.add2", "args": [23, 666]}' \
		http://localhost:8443/call
	@echo ""
