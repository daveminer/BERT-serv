broker_url = 'amqp://guest:guest@localhost:5672'
include = ['sentiment.tasks']
result_backend = 'db+sqlite:///db.sqlite3'
result_expires = 3600
