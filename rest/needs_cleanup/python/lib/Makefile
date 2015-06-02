all:
	@echo "Targets: install, clean, publish"

install:
	python setup.py install

clean:
	rm -rf ./crossbarconnect.egg-info
	rm -rf ./build
	rm -rf ./dist
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -type d -exec rm -rf {} \;

publish: clean
	python setup.py register
	python setup.py sdist upload
