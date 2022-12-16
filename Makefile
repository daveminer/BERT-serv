deps:
	pip install -r requirements.txt
dev:
	./manage.py runserver
test:
	./manage.py test
