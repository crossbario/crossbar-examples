default:
	@echo "Targets:"
	@echo ""
	@echo "   crossbar              Run a TLS router and a TLS client component in a container"
	@echo "   crossbar_shared       Run 2 non-TLS Web workers sharing a TCP listening port"
	@echo "   crossbar_shared_tls   Run 2 TLS Web workers sharing a TCP listening port"

generate_certs:
	./create-self-signed-cert.sh
	./create-certificates.sh

print_cert_fingerprints:
	@echo
	@echo "server:"
	@openssl x509 -noout -in .crossbar/server.crt -fingerprint -sha1
	@echo
	@echo "client0:"
	@openssl x509 -noout -in .crossbar/client0.crt -fingerprint -sha1
	@echo
	@echo "client1:"
	@openssl x509 -noout -in .crossbar/client1.crt -fingerprint -sha1


crossbar:
	crossbar start

crossbar_shared:
	crossbar start --config=config_shared.json

crossbar_shared_tls:
	crossbar start --config=config_shared_tls.json


test_client_tx: test_client_tx_good test_client_tx_bad

test_client_tx_good:
	python client_tx.py --url wss://localhost:8080/ws --channel_binding="tls-unique" --key client0.key --cert client0.crt

test_client_tx_bad:
	python client_tx.py --url wss://localhost:8080/ws --channel_binding="tls-unique" --key client1.key --cert client1.crt
