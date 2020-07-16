#CROSSBAR=${PWD}/.test/bin/crossbarfx
CROSSBAR=crossbarfx

CROSSBAR_FABRIC_SUPERUSER=${HOME}/.crossbarfx/default.pub
CROSSBAR_FABRIC_URL=ws://localhost:9000/ws
CROSSBARFX_WATCH_TO_PAIR=${PWD}/.test/nodes

# see screenshots docs/shot1.png
install_crossbar:
	mkdir -p ${PWD}/.test/bin
	curl https://download.crossbario.com/crossbarfx/linux-amd64/crossbarfx-latest -o crossbarfx
	chmod +x crossbarfx
	mv crossbarfx ${PWD}/.test/bin

init_shell:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} shell init --yes

# see screenshots docs/shot2.png
run_master:
	CROSSBAR_FABRIC_SUPERUSER=${CROSSBAR_FABRIC_SUPERUSER} \
	CROSSBARFX_WATCH_TO_PAIR=${CROSSBARFX_WATCH_TO_PAIR} \
	${CROSSBAR} master start --cbdir=${PWD}/.test/master

# see screenshots docs/shot3.png and docs/shot4.png
run_node1:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1

# see screenshots docs/shot5.png
run_node2:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node2

# see screenshots docs/shot6.png
status_master:
	${CROSSBAR} shell show status
	${CROSSBAR} shell list mrealms
	${CROSSBAR} shell show mrealm default
	${CROSSBAR} shell --realm default list nodes
	${CROSSBAR} shell --realm default show node

configure_cluster:
	crossbarfx shell --realm default create webcluster cluster1 --config='{"tcp_port": 8080, "tcp_shared": true}'
	crossbarfx shell --realm default add webcluster-node cluster1 all --config '{"parallel": 2}'
	crossbarfx shell --realm default add webcluster-service cluster1 "/" --config '{"type": "static", "directory": "..", "options": {"enable_directory_listing": true}}'
	crossbarfx shell --realm default add webcluster-service cluster1 "info" --config '{"type": "nodeinfo"}'
	crossbarfx shell --realm default add webcluster-service cluster1 "settings" --config '{"type": "json", "value": [1, 2, 3]}'

# docs/shot7.png, docs/shot8.png
start_cluster:
	crossbarfx shell --realm default start webcluster cluster1


create_cluster_old:
	crossbarfx shell --realm default create webcluster cluster1 --config='{"tcp_port": 8080, "tcp_shared": true}'
	crossbarfx shell --realm default show node

configure_cluster_old:
	crossbarfx shell --realm default add webcluster-node cluster1 node-1a1f8f39 --config '{"webcluster_oid": "20f98b08-6cfa-4339-a828-0c213885ac46"}'
	crossbarfx shell --realm default add webcluster-node cluster1 node-768f65b8 --config '{"webcluster_oid": "20f98b08-6cfa-4339-a828-0c213885ac46", "parallel": 4}'
	crossbarfx shell --realm default add webcluster-service cluster1 "/" --config '{"type": "static", "directory": "..", "options": {"enable_directory_listing": true}}'
	crossbarfx shell --realm default add webcluster-service cluster1 "info" --config '{"type": "nodeinfo"}'
	crossbarfx shell --realm default add webcluster-service cluster1 "settings" --config '{"type": "json", "value": [1, 2, 3]}'

configure_cluster_add1:
	crossbarfx shell --realm default add webcluster-service cluster1 "other" --config '{"type": "json", "value": {"contents": "settings2"}}'



############################################################################################################

status_nodes:
	${CROSSBAR} shell --realm default show node
	find ${PWD}/.test/nodes -name key.pub -print -exec sh -c "grep 'public-key' {} && crossbarfx edge status --cbdir={}" \;

find_nodes:
	find ${PWD}/.test/nodes -name key.activate -print -exec cat {} \;

run_node1_unmanaged:
	CROSSBAR_FABRIC_URL="" \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1

run_node3:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node3

run_node4:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node4

run_node5:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node5

# WARNING: this will destroy your current CLI config & user profiles folder immediately
# and create a fresh one from scratch!
clean_shell:
	rm -rf ${HOME}/.crossbarfx

clean_master:
	rm -rf ${PWD}/.test/master
	mkdir -p ${PWD}/.test/master

clean_nodes:
	rm -rf ${PWD}/.test/nodes
	mkdir -p ${PWD}/.test/nodes

clean_bin:
	rm -rf ${PWD}/.test/bin
	mkdir -p ${PWD}/.test/bin

clean_profile:
	rm -rf ${HOME}/.crossbarfx

clean: clean_master clean_nodes

clean_all: clean clean_bin clean_profile
