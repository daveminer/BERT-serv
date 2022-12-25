import os

broker_url = os.environ['CELERY_BROKER']
include = ['sentiment.tasks']
result_backend = os.environ['RESULT_BACKEND']
result_expires = 3600
