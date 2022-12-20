coverage-html:
	pytest --cov=. --cov-report=html
deps:
	pip install -r requirements.txt
dev:
	./manage.py runserver
freeze:
	pip freeze > requirements.txt
test:
	./manage.py test
test-ci:
	act
test-ci-coverage:
	act workflow_run --workflows ./.github/workflows/coverage.yml
