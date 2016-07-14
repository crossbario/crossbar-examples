test: build
	crossbar start

requirements:
	npm install

build: build_cpp

build_cpp:
	scons

clean:
	scons -uc
	find . -name "*.pyc" -exec rm -f {} \;
