import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bert_serv.settings')

app = Celery('sentiment')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
