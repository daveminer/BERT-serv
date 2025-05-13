app:
	./manage.py runserver
build-app:
	docker build --target webapp -t bert-serv .
build-worker:
	docker build --target celery_worker -t bert-serv-worker .
coverage-html:
	pytest --cov=. --cov-report=html
deps:
	pip3 install -r requirements.txt
dev:
	docker compose up --detach
dev-services:
	docker compose up --detach celery_worker rabbitmq redis
freeze:
	pip3 freeze > requirements-freeze.txt
migrate:
	./manage.py migrate
run-app:
	docker run -d --name bert-serv --network host bert-serv
run-worker:
	docker run -d --name bert-serv-worker --network host bert-serv-worker
stop-app:
	docker stop bert-serv || true
	docker rm bert-serv || true
stop-worker:
	docker stop bert-serv-worker || true
	docker rm bert-serv-worker || true
test:
	pytest -s .
test-ci:
	act
test-ci-coverage:
	act workflow_run --workflows ./.github/workflows/coverage.yml
worker:
	celery -A sentiment worker --pool=solo --loglevel=INFO
