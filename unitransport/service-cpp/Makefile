test:
	time docker run -it --rm \
		--link crossbar \
		--user 1000 \
		-v ${PWD}/app:/app \
		crossbario/autobahn-cpp:gcc \
		/app/run

build2:
	time docker run -it --rm \
		--link crossbar \
		--user 1000 \
		-v ${PWD}/app:/usr/local/app/examples \
		crossbario/autobahn-cpp:gcc \
		/usr/local/app/examples/run
