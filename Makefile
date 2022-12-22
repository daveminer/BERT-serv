app:
	./manage.py runserver
coverage-html:
	pytest --cov=. --cov-report=html
deps:
	pip3 install -r requirements.txt
dev:
	docker-compose up --detach
freeze:
	pip3 freeze > requirements-freeze.txt
services:
	docker-compose up --detach celery-worker rabbitmq redis
test:
	./manage.py test
test-ci:
	act
test-ci-coverage:
	act workflow_run --workflows ./.github/workflows/coverage.yml
worker:
	celery -A sentiment worker --pool=solo --loglevel=INFO
