deps:
	pip3 install -r requirements.txt
dev:
	./manage.py runserver
freeze:
	pip3 freeze > requirements.txt
test:
	./manage.py test
