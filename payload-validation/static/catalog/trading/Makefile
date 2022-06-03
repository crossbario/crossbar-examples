clean:
	-rm -rf ./build

build:
	mkdir -p build/schema
	mkdir -p build/img
	cp catalog.yaml build/
	cp LICENSE build/
	cp schema/trading.bfbs build/schema/
	cp img/trading.png build/img/
	cd build && zip -9 -r pydefi-trading .
	du -hs build/pydefi-trading.zip
