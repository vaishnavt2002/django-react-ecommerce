from rest_framework import status
from rest_framework.exceptions import APIException

class DomainError(APIException):
    """
    Base class for all expected, business-level errors.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "domain_error"
    default_detail = "A domain error occured"

class ResourceNotFound(DomainError):
    """Raised when a fetched resource doesn't exist"""
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "not_found"
    default_detail = "Resource not found."

class DuplicateResource(DomainError):
    """
    Raised when a uniquesness constraint would be violated
    """

    status_code = status.HTTP_409_CONFLICT
    default_code = "duplicate_resource"
    default_detail = "Resource already exists."

class InvalidOperation(DomainError):
    """
    Raised when a request is well-formed but rejected by business rules
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "invalid_operation"
    default_detail = "Operation is not allowed in current state."

