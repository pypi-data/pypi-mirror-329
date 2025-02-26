"""(C) 2013-2025 Copycat Software, LLC."""

import uuid

from .Utilities import to_str


def get_unique_hashname():
    """Get unique Hash Name."""
    return f"{uuid.uuid4()}"


def get_unique_filename(filename):
    """Get unique File Name."""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return filename


def get_request_id(request):
    """Get or generate Request UD."""
    if hasattr(request, "request_id"):
        return to_str(request.request_id)

    return get_unique_hashname()
