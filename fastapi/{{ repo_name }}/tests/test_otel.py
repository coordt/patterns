""" "Tests for the {{ package_name }}.otel module."""

import pytest
from fastapi import FastAPI
from opentelemetry import trace

from {{ package_name }}.otel import configure_otel
from {{ package_name }}.settings import AppSettings


class TestConfigureOtel:
    """Tests for the configure_otel function."""

    def test_instrumentation_calls_instrument_app(self, mocker):
        """Test that FastAPIInstrumentor.instrument_app is called."""
        # Assemble
        app = FastAPI()
        settings = AppSettings(otel_debug=False)
        mock_instrumentor = mocker.patch("{{ package_name }}.otel.FastAPIInstrumentor.instrument_app")

        # Act
        configure_otel(app, settings)

        # Assert
        mock_instrumentor.assert_called_once_with(app)

    def test_tracer_provider_set_in_debug_mode(self, mocker):
        """Test tracer provider is set in otel debug mode and not in production."""
        # Assemble
        app = FastAPI()
        settings = AppSettings(otel_debug=True, environment="dev")
        mock_tracer_provider = mocker.patch("{{ package_name }}.otel.trace.set_tracer_provider")
        mock_resource_create = mocker.patch("{{ package_name }}.otel.Resource.create")
        mock_batch_processor = mocker.patch("{{ package_name }}.otel.BatchSpanProcessor")
        mock_console_exporter = mocker.patch("{{ package_name }}.otel.ConsoleSpanExporter")

        # Act
        configure_otel(app, settings)

        # Assert
        mock_resource_create.assert_called_once_with(attributes={"service.name": "{{ package_name }}"})
        mock_tracer_provider.assert_called_once()
        mock_batch_processor.assert_called_once()
        mock_console_exporter.assert_called_once()

    def test_configure_otel_no_action_without_settings(self, mocker):
        """Test no action is taken if neither debug nor connection string is provided."""
        app = FastAPI()
        settings = AppSettings(otel_debug=False, otel_connection_string=None)
        mock_set_tracer_provider = mocker.patch("{{ package_name }}.otel.trace.set_tracer_provider")
        mock_instrumentor = mocker.patch("{{ package_name }}.otel.FastAPIInstrumentor.instrument_app")

        configure_otel(app, settings)

        mock_set_tracer_provider.assert_not_called()
        mock_instrumentor.assert_called_once_with(app)
