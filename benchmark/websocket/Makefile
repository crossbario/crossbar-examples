crossbarfx_host_w1:
	crossbarfx edge start --cbdir=./.crossbar --config=config_w1.json

crossbarfx_host_w2:
	crossbarfx edge start --cbdir=./.crossbar --config=config_w2.json

crossbarfx_host_w4:
	crossbarfx edge start --cbdir=./.crossbar --config=config_w4.json

crossbarfx_host_w8:
	crossbarfx edge start --cbdir=./.crossbar --config=config_w8.json

crossbarfx_host_w16:
	crossbarfx edge start --cbdir=./.crossbar --config=config_w16.json


crossbarfx_docker_w1:
	docker run -it --rm \
		--network host \
		-v ${PWD}/.crossbar:/node/.crossbar \
		crossbario/crossbarfx:pypy-slim-amd64 \
		edge start --cbdir=/node/.crossbar --config=config_w1.json

crossbarfx_docker_w2:
	docker run -it --rm \
		-p 8080:8080 \
		-v ${PWD}:/node \
		crossbario/crossbarfx:pypy-slim-amd64 \
		edge start --cbdir=/node/.crossbar --config=config_w2.json

crossbarfx_docker_w4:
	docker run -it --rm \
		-p 8080:8080 \
		-v ${PWD}:/node \
		crossbario/crossbarfx:pypy-slim-amd64 \
		edge start --cbdir=/node/.crossbar --config=config_w4.json

crossbarfx_docker_w8:
	docker run -it --rm \
		-p 8080:8080 \
		-v ${PWD}:/node \
		crossbario/crossbarfx:pypy-slim-amd64 \
		edge start --cbdir=/node/.crossbar --config=config_w8.json

crossbarfx_docker_w16:
	docker run -it --rm \
		-p 8080:8080 \
		-v ${PWD}:/node \
		crossbario/crossbarfx:pypy-slim-amd64 \
		edge start --cbdir=/node/.crossbar --config=config_w16.json


wstest:
	docker run -it --rm \
		--network host \
		-v ${PWD}/test-config:/config \
		-v ${PWD}/test-results:/reports \
		crossbario/autobahn-testsuite \
		/usr/local/bin/wstest --mode fuzzingclient --spec /config/fuzzingclient.json

wsperf:
	k6 run --vus 100 --duration 30s k6-ws-echo.js


# wsperf:
# 	wsperf ws://127.0.0.1:8080 1 10000 1000 2000 ./wsperf-results/results.json

# analyze:
# 	python analyze.py ./wsperf-results/results.json

# test:
# 	wsperf ws://127.0.0.1:8080 8 500000 1000 2000 ./wsperf-results/results_1.json
# #	wsperf ws://127.0.0.1:8080 2 10000 1000 2000 ./wsperf-results/results_2.json
# #	wsperf ws://127.0.0.1:8080 4 10000 1000 2000 ./wsperf-results/results_4.json
# 	python analyze.py ./wsperf-results/results_1.json
# #	python analyze.py ./wsperf-results/results_2.json
# #	python analyze.py ./wsperf-results/results_4.json
