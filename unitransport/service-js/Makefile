test:
	docker run -it --rm \
		--link crossbar \
		--user 1000 \
		-v ${PWD}/app:/app \
		crossbario/autobahn-js \
		/app/run
