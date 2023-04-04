# -*- encoding: utf-8 -*-
from app.handlers.flow_handler import FlowHandler
from app.handlers.help import send_help_message
from app.handlers.invoice import init_invoice_handlers
from app.handlers.start import init_start_handler
from app.handlers.transactions_list import transactions_list_flow_handler
from app.handlers.wallet import init_wallet_handlers
from app.handlers.settings import init_settings_handlers
from utils.message_handler import message_handler

__all__ = (
    'init_handlers',
)


def init_handlers():
    init_start_handler()
    init_invoice_handlers()
    init_settings_handlers()
    init_wallet_handlers()

    @message_handler(
        bot_commands=['help'],
        unauthorized=True,
    )
    async def message_help(context):
        await context.clear_state()
        await send_help_message(context)

    @message_handler(
        bot_commands=['transactions'],
    )
    async def message_transactions(context):
        await transactions_list_flow_handler.start(context)

    @message_handler(
        bot_content_types=['text'],
        bot_callback_func=lambda call: True,
    )
    async def send_text(context):
        flow_handler = FlowHandler.FLOWS.get(context.state.type, None)
        if flow_handler is not None:
            return await flow_handler.handle(context)

        await context.send_message('Unknown message, unknown state ' + (await context.get_message_text()))
        await send_help_message(context)
        await context.clear_state()
