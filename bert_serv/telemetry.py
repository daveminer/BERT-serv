import logging
import os
from opentelemetry import trace
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

def setup_telemetry(resource_name, resource_version: str = "1.0.0"):
    # Set up the tracer provider with service name
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: resource_name,
        ResourceAttributes.SERVICE_VERSION: resource_version
    })
    setup_tracing(resource)
    setup_logging(resource)
    
    # Instrument Django
    DjangoInstrumentor().instrument()
    
    # Instrument Celery
    CeleryInstrumentor().instrument()

def setup_logging(resource: Resource):
    logging.basicConfig(level=logging.INFO)
    LoggingInstrumentor().instrument(
        set_logging_format=True,
        logging_format="%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    )
    
    # Set up logging
    log_exporter = OTLPLogExporter(
        endpoint="api.honeycomb.io:443",
        headers={
            "x-honeycomb-team": os.getenv("HONEYCOMB_API_KEY"),
            "x-honeycomb-dataset": resource.attributes.get(ResourceAttributes.SERVICE_NAME)
        }
    )
    
    # Create logger provider
    logger_provider = LoggerProvider(resource=resource)
    
    # Add processor to logger provider
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add OpenTelemetry handler
    otel_handler = LoggingHandler(logger_provider=logger_provider)
    otel_handler.setLevel(logging.INFO)
    root_logger.addHandler(otel_handler)

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