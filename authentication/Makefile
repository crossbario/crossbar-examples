help: ## Help on available Makefile targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

trunc_log: ## Truncate log file collecting test results ("test.log")
	-rm -f ./test.log
	@date  >> ./test.log
	@echo "" >> ./test.log
	@echo "Crossbar.io WAMP Authentication Test Summary:" >> ./test.log
	@echo "=============================================" >> ./test.log
	@echo "" >> ./test.log

print_log:
	@clear
	@cat ./test.log

test_all: trunc_log test_anonymous test_cookie test_cryptosign test_scram test_ticket test_tls test_wampcra ## Test all WAMP authentication methods
	@clear
	@cat ./test.log

test_anonymous: ## Test WAMP-anonymous
	./test_anonymous.sh
	@cat ./test.log

test_cookie: ## Test WAMP-cookie
	./test_cookie.sh
	@cat ./test.log

test_cryptosign: ## Test WAMP-cryptosign
	./test_cryptosign.sh
	@cat ./test.log

test_scram: ## Test WAMP-scram
	./test_scram.sh
	@cat ./test.log

test_ticket: ## Test WAMP-ticket
	./test_ticket.sh
	@cat ./test.log

test_tls: ## Test WAMP-TLS
	./test_tls.sh
	@cat ./test.log

test_wampcra: ## Test WAMP-CRA
	./test_wampcra.sh
	@cat ./test.log
