venv:
	python3 -m venv venv

install:
	venv/bin/pip install -r requirements.txt

run:
	python3 main.py


setup: venv install run