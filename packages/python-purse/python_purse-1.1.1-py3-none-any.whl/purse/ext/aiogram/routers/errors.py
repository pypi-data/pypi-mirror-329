import functools
import sys
from collections.abc import Awaitable, Callable
from typing import Any, Optional

from aiogram import Bot, F, Router
from aiogram.enums.update_type import UpdateType
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import CallbackQuery, ErrorEvent, Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.markdown import hbold, hcode

from purse import func
from purse.logs.telegram import format_exception

CodeFormatCallable = Callable[[Any], str]
ContextData = dict[str, Any]
HandleForbiddenCallable = Callable[[ErrorEvent], Awaitable[None]]
ExtractContextCallable = Callable[[ErrorEvent], ContextData | Awaitable[ContextData]]


def make_error_router(
    bot: Bot,
    dev_chat_id: int,
    code_fn: CodeFormatCallable = hcode,
    bold_fn: CodeFormatCallable = hbold,
    handle_forbidden_fn: Optional[HandleForbiddenCallable] = None,
    extract_context_fn: Optional[ExtractContextCallable] = None,
    router_name: Optional[str] = "errors",
    handle_key_error: bool = True,
    key_error_message: Optional[str] = None,
    print_exception: bool = True,
    log_exception: bool = True,
) -> Router:
    """Make an error aiogram router."""
    router = Router(name=router_name)

    if handle_key_error is True:
        @router.error(ExceptionTypeFilter(KeyError), F.update.message.as_("message"))
        async def key_error_message_handler(error: ErrorEvent, message: Message):
            """Key Error handler for Message update."""
            exc = error.exception
            bot_name = error.update.message.from_user.username
            text = error.update.message.text
            await bot.send_message(
                dev_chat_id,
                text=(
                    f'Exception: {exc}\n'
                    f'Bot: @{bot_name}\n'
                    f'Message: {code_fn(text)}\n'
                )
            )
            return await message.answer(
                key_error_message or _('An error occurred. Try again later.')
            )

        @router.error(ExceptionTypeFilter(KeyError), F.update.callback_query.as_("query"))
        async def key_error_callback_query_handler(error: ErrorEvent, query: CallbackQuery):
            """Key Error handler for CallbackQuery update."""

            exc = error.exception
            bot_name = error.update.callback_query.message.from_user.username
            text = error.update.callback_query.message.text
            cb_data = error.update.callback_query.data
            await bot.send_message(
                dev_chat_id,
                text=(
                    f'Exception: {exc}\n'
                    f'Bot: @{bot_name}\n'
                    f'Message: {code_fn(text)}\n'
                    f'Callback data: {code_fn(cb_data)}\n'
                )
            )
            return await query.answer(
                key_error_message or _('An error occurred. Try again later.'),
                show_alert=True
            )

    @router.errors()
    async def error_handler(exception: ErrorEvent):
        """Send errors to developer"""

        event_type = exception.update.event_type
        exc_val = exception.exception
        exc = code_fn(exc_val)
        send_msg_to_dev = functools.partial(bot.send_message, chat_id=dev_chat_id)

        ctx = {} if not extract_context_fn else await func.acall(extract_context_fn, exception)
        ctx_text = "\n".join([f"{ctx_key}: {ctx_val}" for ctx_key, ctx_val in ctx.items()])

        if event_type == UpdateType.CALLBACK_QUERY:
            event = exception.update.callback_query
            await send_msg_to_dev(
                text=f"{exc}\n\n"
                     f"Chat ID:  {code_fn(event.message.chat.id)}\n"
                     f"User ID:  {code_fn(event.from_user.id)}\n"
                     f"Message:  \n{code_fn(event.message.text)}\n"
                     f"Callback Data:  {code_fn(event.data)}\n"
                     f"{ctx_text}"
            )

        elif event_type == UpdateType.MESSAGE:
            event = exception.update.message
            await send_msg_to_dev(
                text=f"{exc}\n\n"
                     f"Chat ID:  {code_fn(event.chat.id)}\n"
                     f"User ID:  {code_fn(event.from_user.id)}\n"
                     f"Message:  {code_fn(event.text)}\n"
                     f"{ctx_text}"
            )
        elif isinstance(exc_val, TelegramForbiddenError):
            if handle_forbidden_fn:
                await handle_forbidden_fn(exception)
            return

        else:
            await send_msg_to_dev(text=f"{bold_fn('Error:')}\n{exc}\n{ctx_text}")

        if log_exception:
            sys.stderr.write(
                format_exception(
                    type(exc_val), exc_val, exc_val.__traceback__)
            )

        if print_exception:
            print('an error occurred in telegram context')
            print(
                exception.model_dump_json(
                    indent=2, exclude_none=True,
                    exclude={"exception"},
                    exclude_unset=True,
                    warnings=False,
                ),
            )

    return router
