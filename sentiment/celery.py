import environ
import os
import logging
from celery import Celery
from pathlib import Path
from opentelemetry._logs import set_logger_provider, get_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from bert_serv.telemetry import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bert_serv.settings')
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load from .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Configure logging before creating Celery app
logging.basicConfig(level=logging.INFO)

app = Celery('bert_serv')

app.conf.update(
    broker_connection_retry_on_startup=True
)

app.config_from_envvar('CELERY_CONFIG_MODULE')
app.autodiscover_tasks()

def get_worker_logger():
    """Get a logger configured for Honeycomb logging."""
    # Create a shared logger for both worker and tasks
    logger = logging.getLogger('bert_serv')
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: "bert-serv-worker",
        ResourceAttributes.SERVICE_VERSION: "1.0.0"
    })

    return setup_logging(resource, logger, dataset_name="bert-serv-worker")

# Initialize worker logger
worker_logger = get_worker_logger()

if __name__ == '__main__':
    app.start()
