# -*- encoding: utf-8 -*-
from app.handlers.flow_handler import FlowHandler
from app.state import State
from bot import bot
from utils.keyboard import BotKeyboard

__all__ = (
    'MessageContext',
)


class MessageContext:
    message = None
    state = State()

    db_session = None
    user = None

    def __init__(self, message, callback=None):
        self.message = message
        self.callback = callback

    def get_chat_id(self):
        return self.message.chat.id

    async def get_message_text(self):
        return str(self.message.text).strip()

    async def delete_message(self, message_id=None):
        if message_id is None:
            message_id = self.message.message_id

        return bot.delete_message(self.get_chat_id(), message_id)

    async def send_message(self, text, reply_markup=BotKeyboard.remove(), **kwargs):
        return bot.send_message(self.get_chat_id(), text, reply_markup=reply_markup, **kwargs)

    async def send_document(self, data, reply_markup=BotKeyboard.remove(), **kwargs):
        return bot.send_document(self.get_chat_id(), data, reply_markup=reply_markup, **kwargs)

    async def clear_state(self):
        self.state = State()

    async def start_flow(self, flow):
        assert isinstance(flow, FlowHandler)
        await self.clear_state()

        self.state.type = flow.type
        self.state.step = 0
