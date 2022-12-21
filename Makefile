coverage-html:
	pytest --cov=. --cov-report=html
deps:
	pip3 install -r requirements.txt
dev:
	./manage.py runserver
freeze:
	pip3 freeze > requirements-freeze.txt
services:
	docker-compose up --detach rabbitmq redis
test:
	./manage.py test
test-ci:
	act
test-ci-coverage:
	act workflow_run --workflows ./.github/workflows/coverage.yml
worker:
	celery -A sentiment worker --loglevel=INFO
