.PHONY: test container router

test: container router

container:
	crossbar start --cbdir=./container/working/.crossbar
	crossbar start --cbdir=./container/failure1/.crossbar
	crossbar start --cbdir=./container/failure2/.crossbar
	crossbar start --cbdir=./container/failure3/.crossbar
	crossbar start --cbdir=./container/failure4/.crossbar
	crossbar start --cbdir=./container/failure5/.crossbar
	crossbar start --cbdir=./container/failure6/.crossbar
	crossbar start --cbdir=./container/failure7/.crossbar
	crossbar start --cbdir=./container/failure8/.crossbar

router:
	#crossbar start --cbdir=./router/working/.crossbar
	crossbar start --cbdir=./router/failure1/.crossbar
	crossbar start --cbdir=./router/failure2/.crossbar
	crossbar start --cbdir=./router/failure3/.crossbar
	#crossbar start --cbdir=./router/failure4/.crossbar
	#crossbar start --cbdir=./router/failure5/.crossbar
	#crossbar start --cbdir=./router/failure6/.crossbar
