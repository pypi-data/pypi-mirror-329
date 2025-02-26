"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import logging

from django.http.request import RawPostDataException

# pylint: disable=import-error
from .. import logconst
from ..Utilities import get_client_ip
from ..logformat import Format


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class DjangoLoggingMiddleware:
    """Django Middleware Class for logging Requests and Responses."""

    def __init__(self, get_response):
        """Constructor."""
        self.get_response = get_response

    def __call__(self, request):
        """Docstring."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        log_req, log_res = {}, {}

        # ---------------------------------------------------------------------
        # --- Log Request.
        # ---------------------------------------------------------------------
        log_req.update({
            "http_verb":        request.method,
            "path":             request.get_full_path(),
            "request_get":      request.GET,
            "request_post":     request.POST,
            "request_files":    request.FILES,
            # "request_meta":     request.META,
            "request_headers":  dict(request.headers.items()),
            # "request_session":  dict(request.session.items()),
            "request_user":     request.user,
            "source_ip":        get_client_ip(request),
            "uri":              request.build_absolute_uri(),
        })

        # ---------------------------------------------------------------------
        # --- Assert some extra Attributes in Case of DRF Request.
        try:
            log_req.update({
                "geo_data": request.geo_data,
            })
        except Exception as exc:
            logger.exception("", extra=Format.exception(
                exc=exc,
                request_id=request.request_id,
                log_extra=log_req))

        try:
            log_req.update({
                "request_length":   len(request.body),
            })
        except RawPostDataException:
            pass
        except Exception as exc:
            logger.exception("", extra=Format.exception(
                exc=exc,
                request_id=request.request_id,
                log_extra=log_req))

        try:
            log_req.update({
                "request_data":         request.data,
                "request_query_params": request.query_params,
            })
        except Exception as exc:
            # logger.exception("", extra=Format.exception(
            #     exc=exc,
            #     request_id=request.request_id,
            #     log_extra=log_req))
            pass

        logger.info("REQUEST", extra=Format.api_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_API_REQUEST,
            request_id=request.request_id,
            log_extra=log_req))

        # ---------------------------------------------------------------------
        # --- Log Response.
        # ---------------------------------------------------------------------
        response = self.get_response(request)

        log_res.update({
            "request_user":     request.user,
            "response_code":    response.status_code,
            "response_media_type":  response.charset,
        })

        # ---------------------------------------------------------------------
        # --- Assert some extra Attributes.
        try:
            log_res.update({
                "response_length":  len(response.data),
            })
        except:
            try:
                log_res.update({
                    "response_length":  len(response.content),
                })
            except:
                pass
                # log_res.update({
                #     "response_length":  len(list(response.streaming_content)),
                # })

        logger.info("RESPONSE", extra=Format.api_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_API_REQUEST,
            request_id=request.request_id,
            log_extra=log_res))

        return response

