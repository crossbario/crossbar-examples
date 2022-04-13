help: ## Help on available Makefile targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

trunc_log: ## Truncate log file collecting test results ("test.log")
	-rm -f ./test.log
	@date  >> ./test.log
	@echo "" >> ./test.log
	@echo "Crossbar.io WAMP Authentication Test Summary:" >> ./test.log
	@echo "=============================================" >> ./test.log
	@echo "" >> ./test.log

test_all: trunc_log test_anonymous test_cookie test_cryptosign test_scram test_ticket test_tls test_wampcra ## Test all WAMP authentication methods
	@clear
	@cat ./test.log

test_anonymous: ## Test WAMP-anonymous
	./test_anonymous.sh

test_cookie: ## Test WAMP-cookie
	./test_cookie.sh

test_cryptosign: ## Test WAMP-cryptosign
	./test_cryptosign.sh

test_scram: ## Test WAMP-scram
	./test_scram.sh

test_ticket: ## Test WAMP-ticket
	./test_ticket.sh

test_tls: ## Test WAMP-TLS
	./test_tls.sh

test_wampcra: ## Test WAMP-CRA
	./test_wampcra.sh
