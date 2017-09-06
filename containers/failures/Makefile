.PHONY: test container router

test: container router

container:
	crossbar start --personality=community --cbdir=./container/working/.crossbar
	crossbar start --personality=community --cbdir=./container/failure1/.crossbar
	crossbar start --personality=community --cbdir=./container/failure2/.crossbar
	crossbar start --personality=community --cbdir=./container/failure3/.crossbar
	crossbar start --personality=community --cbdir=./container/failure4/.crossbar
	crossbar start --personality=community --cbdir=./container/failure5/.crossbar
	#crossbar start --personality=community --cbdir=./container/failure6/.crossbar
	crossbar start --personality=community --cbdir=./container/failure7/.crossbar
	crossbar start --personality=community --cbdir=./container/failure8/.crossbar

router:
	#crossbar start --personality=community --cbdir=./router/working/.crossbar
	crossbar start --personality=community --cbdir=./router/failure1/.crossbar
	crossbar start --personality=community --cbdir=./router/failure2/.crossbar
	crossbar start --personality=community --cbdir=./router/failure3/.crossbar
	#crossbar start --personality=community --cbdir=./router/failure4/.crossbar
	#crossbar start --personality=community --cbdir=./router/failure5/.crossbar
	#crossbar start --personality=community --cbdir=./router/failure6/.crossbar
