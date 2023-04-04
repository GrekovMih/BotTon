# -*- encoding: utf-8 -*-

from app.handlers.settings.change_email import settings_change_email_flow_handler
from utils.message_handler import message_handler

__all__ = (
    'init_settings_handlers',
)


def init_settings_handlers():
    @message_handler(
        bot_commands=['change_email'],
    )
    async def message_change_email(context):
        await settings_change_email_flow_handler.start(context)
