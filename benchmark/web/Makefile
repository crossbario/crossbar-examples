# start different numbers of workers on the testee host
crossbar_w1:
	crossbar start --config config_w1.json

crossbar_w2:
	crossbar start --config config_w2.json

crossbar_w4:
	crossbar start --config config_w4.json

crossbar_w8:
	crossbar start --config config_w8.json

crossbar_w16:
	crossbar start --config config_w16.json

crossbar_w32:
	crossbar start --config config_w32.json

crossbar_w40:
	crossbar start --config config_w40.json

crossbar_w48:
	crossbar start --config config_w48.json


# test basic operation from the load host
test_functional:
	curl -s ${TESTEE}/resource?count=10000 | wc -c

# run performance tests on load host
test: test_json test_resource test_static

# test Crossbar.io JSON value path service
test_json:
	weighttp -n 5000000 -c 128 -t 8 -k ${TESTEE}/json
	wrk -c 128 -t 8 --latency -d 60 ${TESTEE}/json

# test Crossbar.io Twisted Web resource path service
test_resource: test_resource_16 test_resource_256 test_resource_4096 test_resource_65536

test_resource_16:
	weighttp -n 5000000 -c 128 -t 8 -k ${TESTEE}/resource?count=16
	wrk -c 128 -t 8 --latency -d 60 ${TESTEE}/resource?count=16

test_resource_256:
	weighttp -n 5000000 -c 128 -t 8 -k ${TESTEE}/resource?count=256
	wrk -c 128 -t 8 --latency -d 60 ${TESTEE}/resource?count=256

test_resource_4096:
	weighttp -n 5000000 -c 128 -t 8 -k ${TESTEE}/resource?count=4096
	wrk -c 128 -t 8 --latency -d 60 ${TESTEE}/resource?count=4096

test_resource_65536:
	weighttp -n 5000000 -c 128 -t 8 -k ${TESTEE}/resource?count=65536
	wrk -c 128 -t 8 --latency -d 60 ${TESTEE}/resource?count=65536

# test Crossbar.io static file path service
test_static:
	weighttp -n 5000000 -c 128 -t 8 -k ${TESTEE}/
	wrk -c 128 -t 8 --latency -d 60 ${TESTEE}/

analyze_1:
	grep -Hi "Requests/sec" results/*
	grep -Hi "Transfer/sec" results/*

analyze:
	cd results && python analyze.py > results.txt

test_bigbox:
	wrk -c 128 -t 8 --latency -d 20 http://127.0.0.1:8080/resource?count=16
	wrk -c 128 -t 8 --latency -d 20 http://127.0.0.1:8080/resource?count=256
	wrk -c 128 -t 8 --latency -d 20 http://127.0.0.1:8080/resource?count=4096
	wrk -c 128 -t 8 --latency -d 20 http://127.0.0.1:8080/resource?count=65536
