BUILD_DIR=./build
FBS_FILES=./src/*.fbs
FBS_OUTPUT=./schema

clean:
	-rm -rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/schema
	mkdir -p $(BUILD_DIR)/img

compile:
	flatc -o $(FBS_OUTPUT) --binary --schema --bfbs-comments --bfbs-builtins $(FBS_FILES)

describe:
	xbrnetwork describe-schema --schema $(FBS_OUTPUT)

build: compile
	cp catalog.yaml $(BUILD_DIR)/
	cp $(FBS_OUTPUT)/*.bfbs $(BUILD_DIR)/schema/
	cp LICENSE $(BUILD_DIR)/
	cp README.md $(BUILD_DIR)/
	cp img/*.png $(BUILD_DIR)/img/
	cd $(BUILD_DIR) && zip -9 -r pydefi-trading .
	du -hs $(BUILD_DIR)/pydefi-trading.zip
