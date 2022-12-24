import os

broker_url = os.environ['CELERY_BROKER']
include = ['sentiment.tasks']
print(os.environ['RESULT_BACKEND'], 'BACKEND')
result_backend = os.environ['RESULT_BACKEND']
result_expires = 3600
