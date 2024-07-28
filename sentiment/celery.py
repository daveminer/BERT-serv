import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bert_serv.settings')
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery('bert_serv')

app.config_from_envvar('CELERY_CONFIG_MODULE')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
