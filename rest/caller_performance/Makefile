# run this on 10.0.1.2
testee:
	crossbar start

testee_multi_worker:
	crossbar start --config=config_multi_worker.json

test_multi_worker:
	wrk -t8 -c1000 -d120s --latency -s wrk/test_add.lua http://10.0.1.2:8080

testee_debug:
	PYTHONPATH=${CROSSBAR_REPOS_ROOT}/crossbar python -m crossbar.controller.cli start --loglevel=verbose

test: test_local test_network

test_local: test_local_sequential test_local_concurrent

test_network: test_network_sequential test_network_concurrent

test_local_sequential:
	@echo "Testing over loopback TCP with single client and sequential requests"
	wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://127.0.0.1:8080
	wrk -t1 -c1 -d30s --latency -s wrk/test_sub.lua http://127.0.0.1:8080
	wrk -t1 -c1 -d30s --latency -s wrk/test_mul.lua http://127.0.0.1:8080
	wrk -t1 -c1 -d30s --latency -s wrk/test_div.lua http://127.0.0.1:8080

test_local_concurrent:
	@echo "Testing over loopback TCP with multiple clients and concurrent requests"
	wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://127.0.0.1:8080
	wrk -t4 -c200 -d30s --latency -s wrk/test_sub.lua http://127.0.0.1:8080
	wrk -t4 -c200 -d30s --latency -s wrk/test_mul.lua http://127.0.0.1:8080
	wrk -t4 -c200 -d30s --latency -s wrk/test_div.lua http://127.0.0.1:8080

# run this on 10.0.1.3
test_network_sequential:
	@echo "Testing over 10GbE TCP with single client and sequential requests"
	wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
	wrk -t1 -c1 -d30s --latency -s wrk/test_sub.lua http://10.0.1.2:8080
	wrk -t1 -c1 -d30s --latency -s wrk/test_mul.lua http://10.0.1.2:8080
	wrk -t1 -c1 -d30s --latency -s wrk/test_div.lua http://10.0.1.2:8080

# run this on 10.0.1.3
test_network_concurrent:
	@echo "Testing over 10GbE TCP with multiple clients and concurrent requests"
	wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
	wrk -t4 -c200 -d30s --latency -s wrk/test_sub.lua http://10.0.1.2:8080
	wrk -t4 -c200 -d30s --latency -s wrk/test_mul.lua http://10.0.1.2:8080
	wrk -t4 -c200 -d30s --latency -s wrk/test_div.lua http://10.0.1.2:8080

# run this on 10.0.1.3
test_shared:
	@echo "Testing over 10GbE TCP with single client and sequential requests"
	wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
	@echo "Testing over 10GbE TCP with multiple clients and concurrent requests"
	wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080

