from celery import Celery
from .models import Sentiment

app = Celery('celery',
             broker='amqp://guest:guest@localhost:5672',
             backend='rpc://')


@app.task
def run_sentiment(sentences):
    Sentiment.run(sentences)

    # Optional configuration, see the application user guide.
    # app.conf.update(
    #     result_expires=3600,
    # )

    # if __name__ == '__main__':
    #     app.start()
