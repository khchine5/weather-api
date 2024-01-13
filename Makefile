
all: install migrate build pm



install:
	python3.10 -m venv venv
	. venv/bin/activate && pip -V
	. venv/bin/activate && pip install -r requirements.txt

install-dev:
	python3.10 -m venv venv
	. venv/bin/activate && pip -V
	. venv/bin/activate && pip install -r dev-requirements.txt

migrate:
	. venv/bin/activate && python manage.py migrate

pm:
	. venv/bin/activate && python manage.py runserver

build:
	rm -rf weather/node_modules/*
	cd weather && npm install && npm run build && cd ..

watch:
	cd weather && yarn run watch
	
test:
	. venv/bin/activate && python manage.py test

sanity-check:
	. venv/bin/activate && black .
	flake8 .
	. venv/bin/activate && isort .

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
