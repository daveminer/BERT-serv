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
migrate:
	./manage.py migrate
services:
	docker-compose up --detach celery_worker db rabbitmq redis
test:
	pytest -s .
test-ci:
	act
test-ci-coverage:
	act workflow_run --workflows ./.github/workflows/coverage.yml
worker:
	celery -A sentiment worker --pool=solo --loglevel=INFO
