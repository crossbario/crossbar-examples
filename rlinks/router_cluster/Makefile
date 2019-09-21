requirements:
	sudo apt update && sudo apt install -y haproxy haproxyctl hatop


run_haproxy:
	haproxy -f haproxy.conf


run_ha_edge1:
	crossbarfx edge start --cbdir ./ha_setup/edge1/.crossbar

run_ha_edge2:
	crossbarfx edge start --cbdir ./ha_setup/edge2/.crossbar

run_ha_edge3:
	crossbarfx edge start --cbdir ./ha_setup/edge3/.crossbar

run_ha_edge4:
	crossbarfx edge start --cbdir ./ha_setup/edge4/.crossbar


run_smp_edge1:
	crossbarfx edge --debug-lifecycle start --vmprof --cbdir ./smp_setup/edge1/.crossbar


run_benchmark:
	python main.py --config client.ini \
		--duration 300 --period 1 --clients 1 --connections 1 --loops 1 --rate 0.25 --stride 1 --size 512

run_benchmark_single:
	python main.py --config client_single.ini \
		--duration 300 --period 1 --clients 1 --connections 1 --loops 1 --rate 0.25 --stride 1 --size 512

run_benchmark_haproxy:
	python main.py --config client_haproxy.ini \
		--duration 300 --period 1 --clients 1 --connections 40 --loops 1 --rate 0.5 --stride 1 --size 512


run_test:
	python main.py --duration 5 --period 1 --clients 1 --connections 1 --loops 1 --rate 1 --stride 1 --size 512


run_all:
	crossbarfx edge --debug-lifecycle start --vmprof --cbdir ./smp_setup/edge1/.crossbar &
	sleep 30
	python main.py
	crossbarfx edge stop --cbdir ./smp_setup/edge1/.crossbar


clean:
	find . -name ".vmprof-*.dat" -exec rm -f {} \;
