# Run a development server without Docker
app:
	./manage.py runserver

# Build a production image of the webapp
build-app:
	docker build --target webapp -t bert-serv .

# Build a production image of the celery worker
build-worker:
	docker build --target celery_worker -t bert-serv-worker .

coverage-html:
	pytest --cov=. --cov-report=html

deps:
	pip3 install -r requirements.txt

# Run the development server with Docker
dev:
	docker compose up --detach

# Run the all of the services besides the webapp in Docker
dev-services:
	docker compose up --detach celery_worker rabbitmq redis

freeze:
	pip3 freeze > requirements-freeze.txt

migrate:
	./manage.py migrate

# Run the production webapp container
run-app:
	docker run -d --name bert-serv --network host bert-serv

# Run the production celery worker container
run-worker:
	docker run -d --name bert-serv-worker --network host bert-serv-worker

# Stop the production webapp container
stop-app:
	docker stop bert-serv || true
	docker rm bert-serv || true

# Stop the production celery worker container
stop-worker:
	docker stop bert-serv-worker || true
	docker rm bert-serv-worker || true

test:
	pytest -s .

# Run the tests in a CI environment
test-ci:
	act

# Run the tests and generate a coverage report in a CI environment
test-ci-coverage:
	act workflow_run --workflows ./.github/workflows/coverage.yml

# Run the celery worker without Docker
worker:
	celery -A sentiment worker --pool=solo --loglevel=INFO
