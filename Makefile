deps:
	pip install -r requirements.txt
dev:
	./manage.py runserver
freeze:
	pip freeze > requirements.txt
test:
	./manage.py test
venv:
	source .venv/bin/activate
