import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

def setup_telemetry():
    # Set up the tracer provider with service name
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: "bert-serv",
        ResourceAttributes.SERVICE_VERSION: "1.0.0"
    })
    tracer_provider = TracerProvider(resource=resource)
    
    # Configure the OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint="api.honeycomb.io:443",
        headers={
            "x-honeycomb-team": os.getenv("HONEYCOMB_API_KEY"),
            "x-honeycomb-dataset": os.getenv("HONEYCOMB_DATASET", "bert-serv")
        }
    )
    
    # Add the span processor to the tracer
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    # Set the tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Instrument Django
    DjangoInstrumentor().instrument()
    
    # Instrument Celery
    CeleryInstrumentor().instrument() 