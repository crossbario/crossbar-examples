# run this on 10.0.1.2
testee:
	crossbar start

# run this on 10.0.1.3
load_add_single:
	wrk -t1 -c1 -d30s --latency -s test_add.lua http://10.0.1.2:8080

# run this on 10.0.1.3
load_add_concurrent:
	wrk -t4 -c200 -d30s --latency -s test_add.lua http://10.0.1.2:8080

# run this on 10.0.1.3
load_mul_single:
        wrk -t1 -c1 -d30s --latency -s test_mul.lua http://10.0.1.2:8080

# run this on 10.0.1.3
load_mul_concurrent:
        wrk -t4 -c200 -d30s --latency -s test_mul.lua http://10.0.1.2:8080

test:
	PYTHONPATH=${CROSSBAR_REPOS_ROOT}/crossbar python -m crossbar.controller.cli start

debug:
	PYTHONPATH=${CROSSBAR_REPOS_ROOT}/crossbar python -m crossbar.controller.cli start --loglevel=verbose
