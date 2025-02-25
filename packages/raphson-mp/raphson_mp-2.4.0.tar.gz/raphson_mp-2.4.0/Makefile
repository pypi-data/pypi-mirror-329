PYTHON=.venv/bin/python
PYBABEL=.venv/bin/pybabel
MUSIC=.venv/bin/raphson-mp

.PHONY: clean test testall update-messages compile-messages deploy-pipy deploy-docker

$(PYTHON):
	python3 -m venv .venv

$(MUSIC): $(PYTHON) pyproject.toml
	$(PYTHON) -m pip install --editable .[full,dev]

clean:
	rm -rf .pytest-cache dist messages.pot

test: $(MUSIC)
	pytest -m "not online"

testall: $(MUSIC)
	$(PYTHON) -m coverage run -m pytest

coverage: $(MUSIC)
	$(PYTHON) -m coverage report

update-messages: $(MUSIC)
	$(PYBABEL) extract --mapping babel.cfg --keyword gettext_lazy --output messages.pot raphson_mp
	$(PYBABEL) update -i messages.pot -d raphson_mp/translations

compile-messages: $(MUSIC)
	$(PYBABEL) compile -d raphson_mp/translations

deploy-pypi: $(MUSIC) clean compile-messages
	python3 -m build
	python3 -m twine upload dist/*

deploy-docker: clean
	docker buildx build -t ghcr.io/danielkoomen/webapp --target prod --push .
	docker buildx build -f Dockerfile.nginx -t ghcr.io/danielkoomen/webapp:nginx --push .

format: $(MUSIC)
	black .
	isort .
