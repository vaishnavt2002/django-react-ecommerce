import uuid
import time
import structlog
from ecommerce.core.logging import get_logger

logger = get_logger(__name__)


class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.META.get('HTTP_X_REQUEST_ID') or str(uuid.uuid4())
        request.request_id = request_id

        # Bind request_id 
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start_time = time.time()

        logger.info(
            "request_started",
            method=request.method,
            path=request.path,
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', 'unknown'),
        )

        try:
            response = self.get_response(request)
        except Exception:
            logger.exception("request_failed", method=request.method, path=request.path)
            structlog.contextvars.clear_contextvars()
            raise

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "request_completed",
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        response['X-Request-ID'] = request_id
        structlog.contextvars.clear_contextvars()
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')