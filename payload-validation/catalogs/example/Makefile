CATALOG_NAME=example

FBS_FILES=./src/*.fbs
FBS_OUTPUT=./schema

BUILD_DIR=./build

# https://blog.infura.io/post/ipfs-file-upload-client-tool
setup_ipfs_client_tool:
	wget https://github.com/INFURA/ipfs-upload-client/releases/download/v0.1.1/ipfs-upload-client-v0.1.1-linux-amd64.tar.gz
	tar xvf ipfs-upload-client-v0.1.1-linux-amd64.tar.gz
	sudo cp ipfs-upload-client /usr/local/bin/

# https://github.com/KittyHawkCorp/stripzip
# https://linux.die.net/man/1/zip
setup_stripzip:
	cd /tmp && git clone https://github.com/KittyHawkCorp/stripzip.git && cd stripzip && make && sudo cp ./stripzip /usr/local/bin/

clean:
	rm -rf $(BUILD_DIR)

distclean: clean
	rm -rf $(FBS_OUTPUT)

compile:
	mkdir -p $(FBS_OUTPUT)
	flatc -o $(FBS_OUTPUT) --binary --schema --bfbs-comments --bfbs-builtins $(FBS_FILES)

describe:
	xbrnetwork describe-schema --schema $(FBS_OUTPUT)

# IMPORTANT: note the use of "-X" and stripzip to preserve privacy and support repeatable builds
build: compile
	@mkdir -p $(BUILD_DIR)/schema
	@mkdir -p $(BUILD_DIR)/img
	@cp catalog.yaml $(BUILD_DIR)/
	@cp $(FBS_OUTPUT)/*.bfbs $(BUILD_DIR)/schema/
	@cp LICENSE.txt $(BUILD_DIR)/
	@cp README.md $(BUILD_DIR)/
	@cp img/*.png $(BUILD_DIR)/img/
	@cd $(BUILD_DIR) && zip -9 -X -r $(CATALOG_NAME) .
	@stripzip $(BUILD_DIR)/$(CATALOG_NAME).zip
	@du -hs $(BUILD_DIR)/$(CATALOG_NAME).zip
	@openssl sha256 $(BUILD_DIR)/$(CATALOG_NAME).zip
	@unzip -l $(BUILD_DIR)/$(CATALOG_NAME).zip

publish:
	ipfs-upload-client --id ${INFURA_IPFS_PROJECT_ID} --secret ${INFURA_IPFS_PROJECT_SECRET} \
		$(BUILD_DIR)/$(CATALOG_NAME).zip

publish_curl:
	curl "https://ipfs.infura.io:5001/api/v0/add?pin=false" \
		-X POST \
		-H "Content-Type: multipart/form-data" \
		-F file=@$(BUILD_DIR)/$(CATALOG_NAME).zip

fetch_catalog:
	@rm -f /tmp/$(CATALOG_NAME).zip
	@curl -X POST --output /tmp/$(CATALOG_NAME).zip \
		https://ipfs.infura.io:5001/api/v0/cat?arg=QmdaWNrsnsQcYxLxMP6bjP2wj5Mjtd7aez8RnnJWZ4uzyJ
	openssl sha256 /tmp/$(CATALOG_NAME).zip
	openssl sha256 $(BUILD_DIR)/$(CATALOG_NAME).zip
