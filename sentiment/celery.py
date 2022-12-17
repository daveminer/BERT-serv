from celery import Celery
from utils import Sentiment

app = Celery('tasks',
             broker='amqp://guest:guest@localhost:5672',
             backend='rpc://')


@app.task
def sentiment(sentences):
    Sentiment.run(sentences)
    # Optional configuration, see the application user guide.
    # app.conf.update(
    #     result_expires=3600,
    # )

    # if __name__ == '__main__':
    #     app.start()
