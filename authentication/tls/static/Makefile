default:
	@echo "Targets:"
	@echo ""
	@echo "   test              Run a TLS router and a TLS client component in a container"
	@echo "   test_shared       Run 2 non-TLS Web workers sharing a TCP listening port"
	@echo "   test_shared_tls   Run 2 TLS Web workers sharing a TCP listening port"

test:
	crossbar start

test_shared:
	crossbar start --config=config_shared.json

test_shared_tls:
	crossbar start --config=config_shared_tls.json
