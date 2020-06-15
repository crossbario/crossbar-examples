default:
	@echo "targets:"
	@echo ""
	@echo "   clean        remove build artifacts"
	@echo "   build        build zip archives"
	@echo "   start        run crossbar"
	@echo "   check        check crossbar config"

clean:
	-rm -f ./home.zip

build:
	cd home && zip ../home.zip * && cd ..
	unzip -l home.zip

check:
	crossbar check

start:
	crossbar start

test:
	@curl -s http://localhost:8080                       | openssl sha256
	@curl -s http://localhost:8080/                      | openssl sha256
	@curl -s http://localhost:8080/index.html            | openssl sha256
	@echo

	@curl -s http://localhost:8080/info                  | openssl sha256
	@curl -s http://localhost:8080/info/                 | openssl sha256
	@echo

	@curl -s http://localhost:8080/config                | openssl sha256
	#curl -s http://localhost:8080/config/
	@echo

	@curl -s http://localhost:8080/ws                    | openssl sha256
	@curl -s http://localhost:8080/ws/                   | openssl sha256
	@echo

	#curl -s http://localhost:8080/nested
	@curl -s http://localhost:8080/nested/               | openssl sha256
	@curl -s http://localhost:8080/nested/index.html     | openssl sha256
	@echo

	@curl -s http://localhost:8080/nested/info           | openssl sha256
	@curl -s http://localhost:8080/nested/info/          | openssl sha256
	@echo

	@curl -s http://localhost:8080/nested/config         | openssl sha256
	#curl -s http://localhost:8080/nested/config/
	@echo

	@curl -s http://localhost:8080/nested/ws             | openssl sha256
	@curl -s http://localhost:8080/nested/ws/            | openssl sha256
	@echo
