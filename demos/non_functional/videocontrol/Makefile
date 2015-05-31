all:
	@echo "Targets:"
	@echo ""
	@echo "test       Start Crossbar node."
	@echo "clean      Clean everything."
	@echo ""

develop:
	# see: http://pythonhosted.org/setuptools/setuptools.html#development-mode
	python setup.py develop

install:
	python setup.py install

test: develop
	crossbar start

clean:
	python setup.py develop --uninstall
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	find . -name "*.pyc" -exec rm -f {} \;
