from .celery import app
from .models import Sentiment

# from celery.contrib import rdb


@app.task
def run_sentiment(sentences):
    # rdb.set_trace()
    Sentiment.run(sentences)
