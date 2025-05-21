"""Main entrypoint for {{ project_name }}."""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from {{ package_name }}.logging_info import configure as configure_logging
from {{ package_name }}.middleware import LogCorrelationIdMiddleware
from {{ package_name }}.otel import configure_otel
from {{ package_name }}.routers import health
from {{ package_name }}.settings import settings

configure_logging()

logger = structlog.get_logger(__name__)

app: FastAPI = FastAPI(
    title=settings.name,
    description=settings.name,
    docs_url="/swagger",
    default_response_class=ORJSONResponse,
    swagger_ui_oauth2_redirect_url="/auth/callback",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(LogCorrelationIdMiddleware)

app.include_router(health.router)

configure_otel(app, settings)
