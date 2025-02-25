import datetime
import functools
import inspect
import logging
import re

from aio_pika.message import Message

from typing import Any, Callable


logger = logging.getLogger(__name__)


def fix_message_timestamp(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(message: Message) -> Any:
        # Fix `pamqp` naive timestamp
        if message.timestamp:
            message.timestamp = message.timestamp.replace(tzinfo=datetime.timezone.utc)

        return func(message)

    return inner


def clean_service_name(service_name: str) -> str:
    return re.sub("[^a-z0-9-]+", "-", service_name.strip().lower())


def assert_handler_is_coroutine(handler: Callable) -> None:
    if not inspect.iscoroutinefunction(handler):
        raise TypeError(f"{handler!r} must be coroutine functions")


def assert_handler_kwargs_only(handler: Callable) -> None:
    positional_only = []
    positional_or_keyword = []

    for parameter_name, parameter in inspect.signature(handler).parameters.items():
        if parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            positional_or_keyword.append(parameter_name)

        elif parameter.kind in [
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.VAR_POSITIONAL,
        ]:
            positional_only.append(parameter_name)

    if positional_only:
        raise TypeError(
            f"{handler!r} has positional-only parameters {positional_only} that are not supported"
        )

    if positional_or_keyword:
        logger.warning(
            "%s has positional parameters %s, only keyword parameters are supported",
            handler,
            positional_or_keyword,
        )
