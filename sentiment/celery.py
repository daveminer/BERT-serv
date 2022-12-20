import os
from celery import Celery
# from celery.contrib import rdb
# from .models import Sentiment

os.environ['DJANGO_SETTINGS_MODULE'] = "bert_serv.settings"

app = Celery('sentiment',
             broker='amqp://guest:guest@localhost:5672',
             include=['sentiment.tasks'])


app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
