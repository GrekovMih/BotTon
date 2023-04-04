# -*- encoding: utf-8 -*-
import traceback

from sentry_sdk import capture_exception

from app.state import get_cached_state, cache_state
from bot import bot
from cracc_database.app.models import scoped_session
from cracc_database.app.models.users import UserModel
from telebot.types import CallbackQuery
from utils.message_context import MessageContext
from utils.thread_local import get_thread_local_loop

__all__ = (
    'message_handler',
)


def message_handler(
        bot_commands=None,
        bot_content_types=None,
        bot_callback_func=lambda call: False,
        unauthorized=False,
):
    def decorator(func):
        async def handler(message):
            print(message)

            try:
                if isinstance(message, CallbackQuery):
                    message_context = MessageContext(message.message, message)
                else:
                    message_context = MessageContext(message)

                message_context.state = await get_cached_state(message_context.get_chat_id())

                async with scoped_session() as db_session:
                    message_context.db_session = db_session

                    user = db_session.query(UserModel) \
                        .filter(UserModel.telegram_id == message.from_user.id) \
                        .first()

                    if user is None and unauthorized is False:
                        user = UserModel()
                        user.telegram_id = message.from_user.id
                        user.first_name = message.from_user.first_name
                        user.last_name = message.from_user.last_name

                        db_session.add(user)
                        db_session.commit()
                        db_session.refresh(user)

                    message_context.user = user

                    await func(message_context)

                await cache_state(message_context.get_chat_id(), message_context.state)

            except Exception as e:
                print(e, traceback.format_exc())
                capture_exception(e)

                try:
                    await message_context.send_message('Cant process message')
                except:
                    pass

        @bot.message_handler(commands=bot_commands, content_types=bot_content_types)
        @bot.callback_query_handler(func=bot_callback_func)
        def inner(message):
            get_thread_local_loop().run_until_complete(handler(message))

    return decorator
