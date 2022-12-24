broker_url = 'amqp://guest:guest@localhost:5672'
include = ['sentiment.tasks']
result_backend = 'db+postgresql+psycopg2://localhost:5432'
result_expires = 3600
