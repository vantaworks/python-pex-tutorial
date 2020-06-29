# Application options
APP_NAME := babble

# Doc options
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build

.PHONY: help
help:
	@echo "Available Options:"
	@echo "    WRITE THIS UP"

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-build
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pex:
	rm -f *.pex
	rm -f requirements.txt

.PHONY: clean
clean: clean-build clean-pyc clean-pex

requirements.txt:
	pip -q install pipreqs
	pipreqs --no-pin

.PHONY: interperter
interperter: requirements.txt
	pip . -q pex
	pex . -o interperter.pex

$(APP_NAME).pex: requirements.txt
	pip install -r requirements.txt
	python setup.py develop
	pex . -o $(APP_NAME).pex -e $(APP_NAME):launcher

.PHONY: dist
dist: $(APP_NAME).pex

.PHONY: run
run: $(APP_NAME).pex
	./$(APP_NAME).pex -c examples/gunicorn.conf.py

.PHONY: prototype
prototype:
	pex -r requirements.txt -- dev.py

dev.pyc:
	python dev.py

.PHONY: clean-pyc dev
dev: dev.pyc

.PHONY: lint
lint:
	pylint babble/*

.PHONY: lint-extras
lint-extras:
	pylint *.py

test: clean-pyc
	echo "NEED A TESTER"

coverage:
	echo "NEED COVERAGE"

coverage-upload:
	echo "NEED COVERAGE UPLOADED"

docs:
	@mkdir -p "$(BUILDDIR)"
	@mkdir -p {"$(BUILDDIR)/doctrees","$(BUILDDIR)/html"}
	$(SPHINXBUILD) -M "html" "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -v

clean-docs:
	@rm -rf "$(BUILDDIR)"

.PHONY: env
env:
	pip install -r requirements.txt

.PHONY: pypi
pypi: clean
	python setup.py sdist
	python setup.py bdist_wheel
	pip install twine
	twine upload dist/*

.PHONY: install
install: clean
	python setup.py install

test_xml_to_json:
	curl -i -H "Content-Type: application/xml" -X POST \
	  -d '<?xml version="1.0" ?><person><name>john</name><age>20</age></person>' \
	  http://127.0.0.1:8080/xml_to_json

test_xml_to_json_socket:
	curl -i -H "Content-Type: application/xml" -X POST \
	  -d '<?xml version="1.0" ?><person><name>john</name><age>20</age></person>' \
	  --unix-socket gunicorn.sock \
	  http://127.0.0.1:8080/xml_to_json

test_json_to_xml:
	curl -i -H "Content-Type: application/json" -X POST \
	  -d '{"userId":"1", "username": "fizz bizz"}' \
	  http://127.0.0.1:8080/json_to_xml
