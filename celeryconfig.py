import os

celery_user = os.getenv('CELERY_USER', 'guest')
celery_password = os.getenv('CELERY_PASSWORD', 'guest')
celery_host = os.getenv('CELERY_HOST', 'localhost')
celery_port = os.getenv('CELERY_PORT', 5672)

db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', 5432)

encoded_celery_password = urllib.parse.quote_plus(celery_password)
encoded_db_password = urllib.parse.quote_plus(db_password)

# Celery config
broker_url = f'amqp://{celery_user}:{encoded_celery_password}@{celery_host}:{celery_port}'
include = ['sentiment.tasks']
result_backend = f'db+postgresql://{db_user}:{encoded_db_password}@{db_host}:{db_port}'
result_expires = 3600
