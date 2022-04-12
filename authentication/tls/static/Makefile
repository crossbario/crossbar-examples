default:
	@echo "Targets:"
	@echo ""
	@echo "   test              Run a TLS router and a TLS client component in a container"
	@echo "   test_shared       Run 2 non-TLS Web workers sharing a TCP listening port"
	@echo "   test_shared_tls   Run 2 TLS Web workers sharing a TCP listening port"

generate_certs:
	./create-self-signed-cert.sh
	./create-certificates.sh

print_cert_fingerprints:
	openssl x509 -noout -in .crossbar/server.crt -fingerprint -sha1
	openssl x509 -noout -in .crossbar/server.crt -fingerprint -sha256
	openssl x509 -noout -in .crossbar/client.crt -fingerprint -sha1
	openssl x509 -noout -in .crossbar/client.crt -fingerprint -sha256

test:
	crossbar start

test_shared:
	crossbar start --config=config_shared.json

test_shared_tls:
	crossbar start --config=config_shared_tls.json
