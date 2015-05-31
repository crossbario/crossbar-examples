all:
	@echo "Targets: crossbar, subscribe, publish"

crossbar:
	crossbar start

subscribe:
	@echo "Opening session"
	curl -H "Content-Type: application/json" -d '{"protocols": ["wamp.2.json"]}' http://127.0.0.1:8080/lp/open
	@echo
	@echo

	@echo "Joining realm"
	curl -H "Content-Type: application/json" -d '[1, "realm1", {"roles": {"subscriber": {}, "publisher": {}}}]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
	curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
	@echo
	@echo

	@echo "Subscribing to topic"
	curl -H "Content-Type: application/json" -d '[32, 1, {}, "com.myapp.topic1"]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
	curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
	@echo
	@echo

	@echo "Waiting for event .."
	curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
	@echo
	@echo

publish:
	@echo "Opening session"
	curl -H "Content-Type: application/json" -d '{"protocols": ["wamp.2.json"]}' http://127.0.0.1:8080/lp/open
	@echo
	@echo

	@echo "Joining realm"
	curl -H "Content-Type: application/json" -d '[1, "realm1", {"roles": {"subscriber": {}, "publisher": {}}}]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
	curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
	@echo
	@echo

	@echo "Publishing event to topic"
	curl -H "Content-Type: application/json" -d '[16, 1, {}, "com.myapp.topic1", ["Hello, world!", 23, 666]]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
	@echo

	@echo "Closing session"
	curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/close
	@echo
