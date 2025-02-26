"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from ..Utilities import to_str
from ..uuids import get_unique_hashname


def get_request_id(request):
    """Get or generate Request UD."""
    if hasattr(request, "request_id"):
        return to_str(request.request_id)

    return get_unique_hashname()


class DjangoRequestIDMiddleware:
    """Django Middleware Class for adding `request_id` to Requests."""

    def __init__(self, get_response):
        """Constructor."""
        self.get_response = get_response

    def __call__(self, request):
        """Docstring."""
        request.request_id = get_request_id(request)
        request.META["X-Correlation-ID"] = request.request_id
        request.META["HTTP_X_REQUEST_ID"] = request.request_id

        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id

        return response
