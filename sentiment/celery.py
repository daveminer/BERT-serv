import environ
import os
import logging
from celery import Celery
from pathlib import Path
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

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
    logger = logging.getLogger('celery.worker')
    
    if os.getenv('HONEYCOMB_API_KEY'):
        # Create resource for the worker
        resource = Resource.create({
            ResourceAttributes.SERVICE_NAME: "bert-serv-worker",
            ResourceAttributes.SERVICE_VERSION: "1.0.0"
        })
        
        # Set up logging to Honeycomb
        log_exporter = OTLPLogExporter(
            endpoint="api.honeycomb.io:443",
            headers={
                "x-honeycomb-team": os.getenv("HONEYCOMB_API_KEY"),
                "x-honeycomb-dataset": "bert-serv-worker"
            }
        )
        
        # Create logger provider
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        
        # Configure logger
        logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Add OpenTelemetry handler
        otel_handler = LoggingHandler(logger_provider=logger_provider)
        otel_handler.setLevel(logging.INFO)
        logger.addHandler(otel_handler)
        
        # Add a test log to verify configuration
        logger.info("Celery worker logging configured", extra={
            "worker_startup": True,
            "service_name": "bert-serv-worker"
        })
    
    return logger

# Initialize worker logger
worker_logger = get_worker_logger()

if __name__ == '__main__':
    app.start()
