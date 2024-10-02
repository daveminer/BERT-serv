import environ
import os
from celery import Celery
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bert_serv.settings')
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load from .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

app = Celery('bert_serv')

app.config_from_envvar('CELERY_CONFIG_MODULE')
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
