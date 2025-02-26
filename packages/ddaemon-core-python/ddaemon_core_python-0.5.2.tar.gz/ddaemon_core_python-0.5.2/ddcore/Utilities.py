"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import asyncio
import inspect
import json
import os
import re
import socket
import struct
import sys

from html.parser import HTMLParser
from urllib.parse import (
    parse_qs,
    urlparse)

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

import requests

from bs4 import BeautifulSoup
from ipware import get_client_ip as get_ip


IPWARE_META_PRECEDENCE_ORDER = [
    "HTTP_X_FORWARDED_FOR", "X_FORWARDED_FOR",  # <client>, <proxy1>, <proxy2>
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
]

URL_VALIDATOR = URLValidator()


# =============================================================================
# ===
# === HELPERS
# ===
# =============================================================================
class MLStripper(HTMLParser):
    """Docstring."""

    def __init__(self):
        """Docstring."""
        super().__init__()

        self.reset()
        self.fed = []

    def handle_data(self, d):
        """Docstring."""
        self.fed.append(d)

    def get_data(self):
        """Docstring."""
        return "".join(self.fed)


def escape_html(html):
    """Escape HTML Code."""
    try:
        s = MLStripper()
        s.feed(html)

        return s.get_data()

    except Exception as exc:
        print(f"### EXCEPTION : {str(exc)}")

    return ""


def escape_string(string):
    """Escape String for MySQL."""
    # return MySQLdb.escape_string(
    #     get_purified_str(
    #         re.sub("[^a-zA-Z0-9 \n\.,]", " ", string)
    #         ))
    # return MySQLdb.escape_string(unicode(string, "utf-8"))
    return get_purified_str(re.sub("[^a-zA-Z0-9 \n\.,]", " ", string))


def get_client_ip(request):
    """Get Client IP Address."""
    client_ip, is_routable = get_ip(
        request,
        request_header_order=IPWARE_META_PRECEDENCE_ORDER)

    if client_ip is None:
        # Unable to get the Client's IP Address.
        pass
    else:
        # We got the client's IP address
        if is_routable:
            # The Client's IP Address is publicly routable on the Internet.
            pass
        else:
            # The Client's IP Address is private.
            pass

    return client_ip


def int_to_ip(a_int):
    """Docstring."""
    return socket.inet_ntoa(struct.pack("!I", a_int))


def ip_to_int(a_ip):
    """Docstring."""
    try:
        return struct.unpack("!I", socket.inet_aton(a_ip))[0]
    except Exception as exc:
        print(f"### EXCEPTION : {str(exc)}")

        return 0


def get_boolean(a_value, default_if_None=False):
    """Docstring."""
    if a_value is None:
        return default_if_None

    if isinstance(a_value, bool):
        return a_value

    # -------------------------------------------------------------------------
    # --- Call the local `to_str()` Method in Case we are messing up with the Bytes String.
    value = to_str(a_value).lower()

    if value in ["1", "yes", "true", "on"]:
        return True

    if value in ["", "0", "no", "false", "off"]:
        return False

    raise ValueError(f"Could Not Parse: {a_value}")


def is_awaitable(obj):
    """Return `True`, if the Object is either `coroutine` or `awaitable`."""
    if sys.version_info >= (3, 5, 0):
        result = inspect.iscoroutinefunction(obj) or inspect.isawaitable(obj)

    elif sys.version_info >= (3, 4, 0) and sys.version_info < (3, 5, 0):
        result = (
            isinstance(obj, asyncio.Future) or
            asyncio.iscoroutine(obj) or
            hasattr(obj, "__await__"))
    else:
        raise Exception(
            f"`isawaitable` is not supported on Python {sys.version_info}")

    return result


def to_int(obj):
    """Convert `bytes` to `int`."""
    if obj is None:
        return None

    try:
        if isinstance(obj, bytes):
            return int(obj.decode())

        return int(obj)

    except (ValueError, AttributeError):
        pass

    return None


def to_str(obj):
    """Convert `bytes` to `str`."""
    if obj is None:
        return None

    if isinstance(obj, bytes):
        return str(obj.decode())

    return str(obj)


def to_dict(obj):
    """Convert `bytes` to `dict`."""
    if obj is None:
        return None

    if isinstance(obj, dict):
        return obj

    try:
        if isinstance(obj, bytes):
            return json.loads(obj.decode().replace("\\n", ""))

        return json.loads(obj)

    except Exception as exc:
        print(f"### EXCEPTION : {str(exc)}")

    return None


def is_ascii(val):
    """Validate, if String contains only ASCII Characters."""
    return all(ord(char) < 128 for char in val)


def to_ascii(val):
    """Convert `unicode` or `bytes` to ASCII String."""
    val = to_str(val)

    return "".join([char for char in val if ord(char) < 128])


def get_purified_str(string=""):
    """Purify String."""
    # -------------------------------------------------------------------------
    # --- Remove special Characters.
    #
    # --- TODO: Had to comment out this Line, because it removes mutated Unicode Characters.
    #           Figure out the Way to remove special Characters, but keep printable Unicode
    #           Characters.
    # string = re.sub("[^a-zA-Z0-9 \n\.,]", " ", string)

    # -------------------------------------------------------------------------
    # --- Remove duplicated and trailing Spaces.
    # -------------------------------------------------------------------------
    try:
        string = re.sub(" +", " ", string.strip())
    except Exception as exc:
        print(f"### EXCEPTION : {str(exc)}")

    return string


def get_youtube_video_id(yt_url):
    """Return "video_id" from YouTube Video URL.

    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US

    Source:
    - http://stackoverflow.com/a/7936523
    """
    query = urlparse(yt_url)

    if query.hostname == "youtu.be":
        return query.path[1:]

    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = parse_qs(query.query)

            return p["v"][0]

        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]

        if query.path[:3] == "/v/":
            return query.path.split("/")[2]


def validate_url(url, try_harder=True):
    """Validate URL."""
    try:
        URL_VALIDATOR(url)
    except ValidationError:
        if try_harder:
            url = "http://" + url
            # --- Recursive Run to check a Correctness of the modified URL.
            return validate_url(url, try_harder=False)

        return False

    return url


def get_website_title(url):
    """Get Website Title."""
    try:
        res = requests.get(url, timeout=10)
    except (
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema):
        try:
            res = requests.get("http://" + url, timeout=10)
        except Exception as exc:
            print(f"### EXCEPTION : {str(exc)}")

            return None

    except Exception as exc:
        print(f"### EXCEPTION : {str(exc)}")

        return None

    if res.status_code != 200:
        return None

    try:
        soup = BeautifulSoup(res.text)
        title = soup.title.string.strip()
    except Exception as exc:
        print(f"### EXCEPTION : {str(exc)}")

        return None

    return title


def make_json_cond(name, value):
    """Docstring."""
    cond = json.dumps({
        name:   value
    })[1:-1]  # remove "{" and "}"

    return " " + cond  # avoid '\"'
