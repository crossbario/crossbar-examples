default:
	@echo "targets:"
	@echo ""
	@echo "   clean        remove build artifacts"
	@echo "   build        build zip archives"
	@echo "   test         run crossbar"

clean:
	-rm -f ./.crossbar/*.zip

build:
	cd web1 && zip -r ../.crossbar/web1.zip .
	unzip -l .crossbar/web1.zip
	cd web2 && zip -r ../.crossbar/web2.zip .
	unzip -l .crossbar/web2.zip

test:
	crossbar start --config=config.json
