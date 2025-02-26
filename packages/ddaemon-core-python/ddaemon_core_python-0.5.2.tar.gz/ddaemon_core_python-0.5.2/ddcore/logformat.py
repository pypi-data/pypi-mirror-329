"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import json
import os
import sys

from django.conf import settings

import json_log_formatter

from decouple import config

from .Serializers import JSONEncoder

from . import logconst


class VerboseJSONFormatter(json_log_formatter.VerboseJSONFormatter):
    """Docstring."""

    def json_record(self, message, extra, record):
        """Docstring."""
        extra.update({
            "unixtime":     int(record.created),
        })
        return super().json_record(message, extra, record)


class Format:
    """Helper Class for formatting Logs of specific Types."""

    CENSORED_KEYS = ("email", "username", "password", "retry")

    MIN_MASKED_STARS = 3
    MAX_MASKED_STARS = 16
    MAX_MASKED_CHARS = 3

    @classmethod
    def exception(cls, exc, request_id=None, log_extra=None, **kwargs):
        """Format Exceptions with a Traceback Information.

        Parameters
        ----------
        exc                 :obj        Exception Object.
        request_id          :int        Request ID.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        _, _, exc_tb = sys.exc_info()

        log_extra.update({
            logconst.LOG_KEY_EXC_TYPE:      type(exc).__name__,
            logconst.LOG_KEY_EXC_MSG:       str(exc),
            logconst.LOG_KEY_EXC_TRACEBACK: exc_tb,
        })

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_EXCEPTION,
            log_extra=log_extra,
            file=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1],
            line=exc_tb.tb_lineno,
            request_id=request_id,
            **kwargs)

    @classmethod
    def api_detailed_info(
            cls, log_type=None, request_id=None, log_extra=None, **kwargs):
        """Format API Logs with additional Details.

        Parameters
        ----------
        log_type            :str        Log Type.
        request_id          :int        Request ID.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=log_type or logconst.LOG_VAL_TYPE_API_REQUEST,
            log_extra=log_extra,
            request_id=request_id,
            **kwargs)

    @classmethod
    def daemon_detailed_info(cls, daemon_name, operation, log_extra=None, **kwargs):
        """Format Daemon Logs with additional Details.

        Parameters
        ----------
        daemon_name         :str
        operation           :str
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_DAEMON_REQUEST,
            log_extra=log_extra,
            service=daemon_name,
            operation=operation,
            exception_message=kwargs.pop("exception_message", None),
            error=kwargs.pop("error", None),
            request_id=kwargs.pop("request_id", ""),
            status=kwargs.pop("status", logconst.LOG_VAL_STATUS_SUCCESS),
            **kwargs)

    @classmethod
    def db_error(cls, message, e0, e1, log_extra=None, **kwargs):
        """Format Database Error Logs with additional Details.

        Parameters
        ----------
        message             :str
        e0                  :obj        Error Information.
        e1                  :obj        Error Information.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_DB_ERROR,
            log_extra=log_extra,
            message=message,
            error_0=e0,
            error_1=e1)

    @classmethod
    def outage(cls, component, message="", log_extra=None, **kwargs):
        """Format Outage Logs with additional Details.

        Parameters
        ----------
        component           :obj        Service Component.
        message             :obj        Message.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        return cls.log_detailed_info(
            log_type=logconst.LOG_VAL_TYPE_OUTAGE,
            log_extra=log_extra,
            component=component,
            message=message)

    @classmethod
    def log_detailed_info(cls, log_type, log_extra=None, **kwargs):
        """Append Type Attribute to the Log Record.

        Parameters
        ----------
        log_type            :str        Log Type.
        log_extra           :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        if log_extra is None:
            log_extra = {}

        log_extra.update({
            logconst.LOG_KEY_ABS:                   log_type,
            logconst.LOG_KEY_ABS_ENV:               settings.ENVIRONMENT,
            logconst.LOG_KEY_NEW_RELIC_APP_NAME:    config("NEW_RELIC_APP_NAME", default="Unknown"),
            **kwargs,
        })

        # ---------------------------------------------------------------------
        return json.loads(
            json.dumps(
                dict(sorted(cls.validation(log_extra).items(), key=lambda item: item[0])),
                cls=JSONEncoder))

    @classmethod
    def validation(cls, param_dict: dict):
        """Mask/redact sensitive Data.

        Parameters
        ----------
        param_dict          :dict       Extra logging Dictionary.

        Returns
        -------
                            :dict
        Raises
        ------

        """
        censored_param_dict = param_dict.copy()

        for key, val in censored_param_dict.items():
            # -------------------------------------------------------------
            # --- Parse nested Dictionaries.
            if isinstance(val, dict):
                censored_param_dict[key] = cls.validation(val)
            elif (
                    key in cls.CENSORED_KEYS and
                    isinstance(val, str)):
                if len(val) < 5:
                    censored_param_dict[key] = "*" * len(val)
                else:
                    # --- Calculate Number of Characters around the redacted String.
                    trail_chars = min(cls.MAX_MASKED_CHARS, (len(val) - cls.MIN_MASKED_STARS)//2)

                    # --- Calculate Number of Stars in the redacted String.
                    trail_stars = min(cls.MAX_MASKED_STARS, len(val[trail_chars:-trail_chars]))

                    censored_param_dict[key] = f"{val[:trail_chars]}{'*' * trail_stars}{val[-trail_chars:]}"

        return censored_param_dict
