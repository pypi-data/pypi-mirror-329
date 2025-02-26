"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import datetime
import traceback

from decimal import Decimal
from inspect import istraceback

from django.core.serializers.json import DjangoJSONEncoder


class JSONEncoder(DjangoJSONEncoder):
    """A custom Encoder extending the DjangoJSONEncoder."""

    def default(self, o):
        """Docstring."""
        if istraceback(o):
            return "".join(traceback.format_tb(o)).strip()

        if isinstance(o, (Exception, type)):
            return str(o)

        if isinstance(o, Decimal):
            return str(o)

        if isinstance(o, datetime.datetime):
            if o.tzinfo:
                return o.strftime("%Y-%m-%dT%H:%M:%S%z")

            return o.strftime("%Y-%m-%dT%H:%M:%S")

        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, datetime.time):
            if o.tzinfo:
                return o.strftime("%H:%M:%S%z")

            return o.strftime("%H:%M:%S")

        try:
            return super(DjangoJSONEncoder, self).default(o)
        except TypeError:
            try:
                return str(o)
            except Exception:
                return None


encoder = JSONEncoder(
    indent=4,
    sort_keys=True)
