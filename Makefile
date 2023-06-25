.PHONY: init
init: create_env install-requirements

.PHONY: create_env
create_env:
	python3.8 -m venv env

.PHONY: install-requirements
install-requirements:
	env/bin/python3 -m pip install pip==19.3.1 && env/bin/pip3 install -r requirements.txt

.PHONY: test
test:
	env/bin/python3 -m unittest discover tests
