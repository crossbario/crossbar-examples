default:
	@echo "Targets: check, upgrade"

# find and check all local node configuration files in this repo
check:
	find . -name "config.json" -exec crossbar check --cbdir={} \;

# find and upgrade (if needed) all local node configuration files in this repo
upgrade:
	find . -name "config.json" -exec crossbar upgrade --cbdir={} \;
