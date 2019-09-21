.PHONY: node1 node2 node3 node4 node5

CROSSBAR=crossbarfx
#CROSSBAR=${HOME}/crossbarfx

default:
	@echo 'targets: version node1 node2 node3 node4 node5'

version:
	$(CROSSBAR) edge version

node1:
	cd node1 && $(CROSSBAR) edge start --loglevel=info

node2:
	cd node2 && $(CROSSBAR) edge start --loglevel=info

node3:
	cd node3 && $(CROSSBAR) edge start --loglevel=info

node4:
	cd node4 && $(CROSSBAR) edge start --loglevel=info

node5:
	cd node5 && $(CROSSBAR) edge start --loglevel=info
