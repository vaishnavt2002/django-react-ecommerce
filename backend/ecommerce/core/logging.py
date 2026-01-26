import logging
import structlog
from django.conf import settings
from contextvars import ContextVar

request_id_ctx: ContextVar[str | None] = ContextVar('request_id', default=None)
user_id_ctx: ContextVar[int | None] = ContextVar('user_id', default=None)
def configure_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if settings.ENV == 'production' else structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True
    )

def get_logger(name: str):
    return structlog.get_logger(name)

def set_request_context(request_id: str, user_id: int | None = None):
    request_id_ctx.set(request_id)
    if user_id:
        user_id_ctx.set(user_id)
    
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        user_id=user_id
    )

def clear_request_context():
    request_id_ctx.set(None)
    user_id_ctx.set(None)
    structlog.contextvars.clear_contextvars()