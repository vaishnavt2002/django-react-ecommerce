from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ValidationError as DRFValidationError,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied as DRFPermissionDenied,
    NotFound,
    MethodNotAllowed,
    Throttled,
)

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_handler

from ecommerce.core.logging import get_logger

logger = get_logger(__name__)

_DRF_CODE_MAP = {
    NotAuthenticated:     "not_authenticated",
    AuthenticationFailed: "authentication_failed",
    DRFPermissionDenied:  "permission_denied",
    NotFound:             "not_found",
    MethodNotAllowed:     "method_not_allowed",
    Throttled:            "throttled",
    DRFValidationError:   "validation_failed",
}

def custom_exception_handler(exc, context):

    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=_django_validation_to_dict(exc))

    response = drf_default_handler(exc, context)

    if response is None:
        return _handle_unexpected(exc, context)
    
    code = _resolve_code(exc)

    message, details = _split_message_and_details(response.data)

    response.data = {
        "error":{
            "code": code,
            "message": message,
            "details": details
        }
    }

    logger.info(
        "api_error_response",
        code=code,
        status_code=response.status_code,
        path=_path(context),
        method=_method(context),
        view=_view_name(context),
    )
    return response


def _django_validation_to_dict(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    if hasattr(exc, "messages"):
        return {"non_field_errors": exc.messages}
    return {"non_field_errors": [str(exc)]}

def _handle_unexpected(exc, context):
    logger.error(
        "unexpected_exception",
        exc_type=type(exc).__name__,
        path=_path(context),
        method=_method(context),
        view=_view_name(context),
        exc_info=True
    )

    return Response(
        {
            "error": {
                "code": "internal_error",
                "message": "An unexpected error occured.",
                "details": None
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

def _path(context):
    return context["request"].path if context.get("request") else None

def _method(context):
    return context["request"].method if context.get("request") else None

def _view_name(context):
    view = context.get("view")
    return view.__class__.__name__ if view else None

def _resolve_code(exc):

    if isinstance(exc, DRFValidationError):
        return _DRF_CODE_MAP[DRFValidationError]

    if isinstance(exc, APIException):
        codes = exc.get_codes()
        extracted = _extract_code(codes)
        if extracted and extracted != "invalid":
            return extracted

        if exc.default_code and exc.default_code != "invalid":
            return exc.default_code

    for exc_type, code in _DRF_CODE_MAP.items():
        if isinstance(exc, exc_type):
            return code

    return "error"


def _extract_code(codes):
    if isinstance(codes, str):
        return codes
    if isinstance(codes, list) and codes:
        return _extract_code(codes[0])
    if isinstance(codes, dict) and codes:
        first_value = next(iter(codes.values()))
        return _extract_code(first_value)
    return None

def _split_message_and_details(data):
    if isinstance(data, dict) and "detail" in data and len(data) == 1:
        return str(data["detail"]), None
    
    if isinstance(data, dict) and "non_field_errors" in data:
        errors = data["non_field_errors"]
        if isinstance(errors, list) and errors:
            return str(errors[0]), data
        return str(errors), data
    
    if isinstance(data, dict) and data:
        first_field, first_value = next(iter(data.items()))
        return _flatten_field_error(first_field, first_value), data
    
    if isinstance(data, list) and data:
        return str(data[0]), {"errors": data}

    return str(data), None

    
def _flatten_field_error(field, value):
    if isinstance(value, list) and value:
        first = value[0]
        if isinstance(first, dict):
            inner_field, inner_value = next(iter(first.items()))
            return _flatten_field_error(f"{field}[0].{inner_field}", inner_value)
        
        return f"{field}: {first}"
    
    if isinstance(value, dict) and value:
        inner_field, inner_value = next(iter(value.items()))
        return _flatten_field_error(f"{field}.{inner_field}", inner_value)

    return f"{field}: {value}"