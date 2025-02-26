"""(C) 2013-2025 Copycat Software, LLC. All Rights Reserved."""

import functools
import logging
import tracemalloc

from functools import wraps
from time import perf_counter

from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed)
from django.http import HttpRequest

from termcolor import cprint

from . import logconst
from .logformat import Format


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def log_default(
        _func=None, *, my_logger: logging.Logger = None, cls_or_self=True):
    """Default logging Decorator.

    Parameters
    ----------
    _func                   :obj        Function Object.
    my_logger               :obj        Logger Object.
    cls_or_self             :bool       Is a Class or Instance Method?
    verbose                 :bool       Is a Verbosity?

    Returns
    -------

    Raises
    ------
    """
    def log_default_info(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # -----------------------------------------------------------------
            # --- Initials.
            # -----------------------------------------------------------------
            # --- Manage `self` or `cls`.
            _args = list(args)
            _self = None

            if cls_or_self:
                _self = _args.pop(0)

            func_name = f"{_self.__class__.__name__}.{func.__name__}" if _self else func.__name__

            # -----------------------------------------------------------------
            # --- Manage Logger.
            logger = my_logger
            if my_logger is None:
                logger = logging.getLogger(func.__name__)

            log_type = logconst.LOG_VAL_TYPE_FUNC_CALL
            log_extra = {
                "func_name":                func_name,
                "func_args":                _args,
                "func_kwargs":              kwargs,
                "logger":                   logger,
                logconst.LOG_KEY_STATUS:    logconst.LOG_VAL_STATUS_SUCCESS,
            }

            # -----------------------------------------------------------------
            # --- Manage Request and Response.
            request_id = None
            for a in _args:
                if isinstance(a, HttpRequest):
                    log_type = logconst.LOG_VAL_TYPE_FRONT_END_REQUEST
                    request_id = a.request_id
                    break

            # -----------------------------------------------------------------
            # --- Logging.
            # -----------------------------------------------------------------
            cprint(f"***" * 27, "green")
            cprint(f"*** INSIDE  `{func_name}`", "green")

            args_repr = "\n                        ".join([repr(a) for a in _args])
            kwargs_repr = "\n                        ".join([f"{k}={v!r}" for k, v in kwargs.items()])

            cprint(f"    [--- DUMP ---]   ARGS : {args_repr}", "yellow")
            cprint(f"                   KWARGS : {kwargs_repr}", "yellow")

            try:
                tracemalloc.start()
                start_time = perf_counter()
                res = func(*args, **kwargs)
                return res
            except Exception as exc:
                cprint(f"### EXCEPTION @ `{func_name}`:\n"
                       f"                 {type(exc).__name__}\n"
                       f"                 {str(exc)}", "white", "on_red")

                log_extra[logconst.LOG_KEY_STATUS] = logconst.LOG_VAL_STATUS_FAILURE
                logger.exception("", extra=Format.exception(
                    exc=exc,
                    request_id=request_id,
                    log_extra=log_extra))

                raise exc
            else:
                pass
            finally:
                current, peak = tracemalloc.get_traced_memory()
                end_time = perf_counter()
                tracemalloc.stop()

                cprint(f"*** LEAVING   `{func_name}`", "green")
                cprint(f"*** MEM USE  : {current / 10**6:.6f} MB", "yellow")
                cprint(f"    MEM PEAK : {peak / 10**6:.6f} MB", "yellow")
                cprint(f"    TOOK     : {end_time - start_time:.6f} sec", "yellow")
                cprint(f"***" * 27, "green")

                log_extra.update({
                    logconst.LOG_KEY_ABS_EXEC_TIME: f"{end_time - start_time:.6f}",
                    logconst.LOG_KEY_ABS_MEM_USAGE: f"{current / 10**6:.6f}",
                    logconst.LOG_KEY_ABS_MEM_PEAK:  f"{peak / 10**6:.6f}",
                })
                logger.info("", extra=Format.api_detailed_info(
                    log_type=log_type,
                    request_id=request_id,
                    log_extra=log_extra))

        return wrapper

    if _func is None:
        return log_default_info

    return log_default_info(_func)


# Original Idea: http://djangosnippets.org/snippets/2124/
def autoconnect(cls):
    """Class Decorator.

    Automatically connects pre_save / post_save signals on a model class to its
    pre_save() / post_save() methods.
    """
    def connect(signal, func):
        """Docstring."""
        cls.func = staticmethod(func)

        @wraps(func)
        def wrapper(sender, **kwargs):
            """Docstring."""
            return func(kwargs.get("instance"), **kwargs)

        signal.connect(wrapper, sender=cls)

        return wrapper

    if hasattr(cls, "pre_save"):
        cls.pre_save = connect(pre_save, cls.pre_save)

    if hasattr(cls, "post_save"):
        cls.post_save = connect(post_save, cls.post_save)

    if hasattr(cls, "pre_delete"):
        cls.pre_delete = connect(pre_delete, cls.pre_delete)

    if hasattr(cls, "post_delete"):
        cls.post_delete = connect(post_delete, cls.post_delete)

    if hasattr(cls, "m2m_changed"):
        cls.m2m_changed = connect(m2m_changed, cls.m2m_changed)

    return cls
