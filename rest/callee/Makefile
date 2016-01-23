crossbar:
	PYTHONPATH=../../crossbar python -m crossbar.controller.cli start

curl:
	curl -H "Content-Type: application/json" \
		-d '{"procedure": "com.myapp.rest", "kwargs": {"url": "get", "method": "GET"}}' \
		http://127.0.0.1:8080/call
