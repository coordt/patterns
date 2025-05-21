"""Open Telemetry configuration."""

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from {{ package_name }}.settings import AppSettings


def configure_otel(app: FastAPI, settings: AppSettings):
    """Configure OpenTelemetry."""
    if settings.otel_debug and not settings.is_production:
        resource = Resource.create(attributes={SERVICE_NAME: "{{ package_name }}"})

        tracer_provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        tracer_provider.add_span_processor(processor)
        trace.set_tracer_provider(tracer_provider)
    elif settings.otel_connection_string:
        pass

    FastAPIInstrumentor.instrument_app(app)
