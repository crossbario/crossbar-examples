default:
	@echo "Targets: check, upgrade"

# find and check all local node configuration files in this repo
check:
	find . -name "config.json" -exec crossbar check --cbdir={} \;

# find and upgrade (if needed) all local node configuration files in this repo
upgrade:
	find . -name "config.json" -exec crossbar upgrade --cbdir={} \;

fix_autoping:
	find . -type f -name "config*.json" -exec sed -i \
		's/"auto_ping_size": 4/"auto_ping_size": 12/g' {} \;
