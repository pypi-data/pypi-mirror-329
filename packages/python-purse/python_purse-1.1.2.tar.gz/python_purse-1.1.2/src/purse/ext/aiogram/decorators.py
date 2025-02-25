import functools
from typing import Awaitable, Callable, Optional, ParamSpec, TypeVar

from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNotFound,
)

import purse.logs

logger = purse.logs.logger_factory('ext.aiogram.decorators', include_project=True)

P = ParamSpec("P")
T = TypeVar("T")

ToDecorate = Callable[[P], Awaitable[T]]
Decorated = Callable[[P], Awaitable[Optional[T]]]


def tg_pass(func: ToDecorate) -> Decorated:
    """A decorator that make func ignore some aiogram exceptions"""

    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> Optional[T]:
        try:
            result = await func(*args, **kwargs)
        except (TelegramBadRequest, TelegramNotFound, TelegramForbiddenError, Exception) as ex:
            return logger.error(f"{func.__module__}.{func.__name__}: {ex}")

        return result

    return _wrapper
