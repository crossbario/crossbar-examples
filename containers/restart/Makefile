default:
	@echo "targets: all valid_uri invalid_uri"

all: valid_uri invalid_uri

valid_uri:
	-crossbar start --config config-valid-uri.json

invalid_uri:
	-crossbar start --config config-invalid-uri.json
