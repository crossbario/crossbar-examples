build: build_cpp

build_cpp:
	scons

install:
	npm install

clean:
	scons -uc
	find . -name "*.pyc" -exec rm -f {} \;

test:
	crossbar start
