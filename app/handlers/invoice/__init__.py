# -*- encoding: utf-8 -*-
from app.handlers.invoice.create import invoice_create_flow_handler
from utils.message_handler import message_handler

__all__ = (
    'init_invoice_handlers',
)


def init_invoice_handlers():
    @message_handler(
        bot_commands=['invoice_create'],
    )
    async def message_invoice_create(context):
        await invoice_create_flow_handler.start(context)
