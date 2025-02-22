import uuid

import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class FlaskRequestContextMiddleware:
    """Middleware for Flask to add request context to structlog."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """Middleware logic executed for every HTTP request."""

        request_id = environ.get("HTTP_X_REQUEST_ID", str(uuid.uuid4()))
        request_method = environ.get("REQUEST_METHOD", "UNKNOWN")
        request_path = environ.get("PATH_INFO", "")

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            request_method=request_method,
            request_path=request_path,
        )

        return self.app(environ, start_response)


async def add_request_context_fastapi(request: Request, call_next):
    """Middleware for FastAPI applications."""
    request_id = request.headers.get("x-amzn-trace-id")
    if not request_id:
        request_id = str(uuid.uuid4())

    structlog.contextvars.bind_contextvars(
        request_id=request_id, request_method=request.method, request_path=str(request.url)
    )
    response = await call_next(request)
    structlog.contextvars.clear_contextvars()
    return response


class FastAPIRequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware class for FastAPI using BaseHTTPMiddleware."""

    async def dispatch(self, request: Request, call_next):
        return await add_request_context_fastapi(request, call_next)
