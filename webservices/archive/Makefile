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
