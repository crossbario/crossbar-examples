crossbar:
	PYTHONPATH=../../crossbar python -m crossbar.controller.cli start

curl:
	curl -H "Content-Type: application/json" \
		-d '{"topic": "com.myapp.topic1", "args": ["Hello, world"]}' \
		http://127.0.0.1:8080/publish
