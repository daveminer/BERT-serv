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
    
    if os.getenv('HONEYCOMB_API_KEY'):
        try:
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
                },
                insecure=False  # Ensure we're using TLS
            )
            
            # Create a local logger provider for the worker
            logger_provider = LoggerProvider(resource=resource)
            logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
            
            # Configure logger
            logger.setLevel(logging.INFO)
            
            # Remove any existing handlers
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            
            # Add OpenTelemetry handler with local provider
            otel_handler = LoggingHandler(
                level=logging.INFO,
                logger_provider=logger_provider
            )
            logger.addHandler(otel_handler)
            
            # Add a test log to verify configuration
            logger.info("Celery worker logging configured", extra={
                "worker_startup": True,
                "service_name": "bert-serv-worker"
            })
            
        except Exception as e:
            logger.error(f"Failed to configure Honeycomb logging: {str(e)}", exc_info=True)
            # Fall back to basic logging
            basic_handler = logging.StreamHandler()
            basic_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(basic_handler)
    
    return logger

# Initialize worker logger
worker_logger = get_worker_logger()

if __name__ == '__main__':
    app.start()
