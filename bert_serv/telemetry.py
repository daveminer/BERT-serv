import logging
import os
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

def setup_telemetry(resource_name, resource_version: str = "1.0.0", dataset_name: str = "bert-serv"):
    # Set up the tracer provider with service name
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: resource_name,
        ResourceAttributes.SERVICE_VERSION: resource_version
    })
    setup_tracing(resource)
    setup_logging(resource, logging.getLogger(), dataset_name)
    
    # Instrument Django
    DjangoInstrumentor().instrument()
    
    # Instrument Celery
    CeleryInstrumentor().instrument()

def setup_logging(resource: Resource, logger: logging.Logger, dataset_name: str):
    # Verify environment variables
    honeycomb_api_key = os.getenv("HONEYCOMB_API_KEY")
    if not honeycomb_api_key:
        logging.error("HONEYCOMB_API_KEY environment variable is not set")
        return

    service_name = resource.attributes.get(ResourceAttributes.SERVICE_NAME)
    if not service_name:
        logging.error("Service name is not set in resource attributes")
        return

    # Set up logging
    log_exporter = OTLPLogExporter(
        endpoint="api.honeycomb.io:443",
        headers={
            "x-honeycomb-team": honeycomb_api_key,
            "x-honeycomb-dataset": dataset_name
        },
        insecure=False  # Ensure we're using TLS
    )
    
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    # Configure root logger
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add OpenTelemetry handler
    otel_handler = LoggingHandler(logger_provider=logger_provider)
    otel_handler.setLevel(logging.INFO)
    logger.addHandler(otel_handler)

    # Add a test log message
    logging.info("OpenTelemetry logging configured successfully", extra={
        "service.name": service_name,
        "honeycomb_dataset": service_name
    })
    
    # Instrument logging after setting up the handler

    LoggingInstrumentor().instrument(
        set_logging_format=True,
        logging_format="%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    )

    return logger




def setup_tracing(resource: Resource):
    tracer_provider = TracerProvider(resource=resource)
    
    # Configure the OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint="api.honeycomb.io:443",
        headers={
            "x-honeycomb-team": os.getenv("HONEYCOMB_API_KEY"),
            "x-honeycomb-dataset": resource.attributes.get(ResourceAttributes.SERVICE_NAME)
        }
    )
    
    # Add the span processor to the tracer
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    # Set the tracer provider
    trace.set_tracer_provider(tracer_provider)