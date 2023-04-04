# -*- encoding: utf-8 -*-
import re
from _decimal import Decimal

from cracc_database.app.models.invoices import InvoiceModel, InvoiceStatus
from cracc_database.services.invoices import load_invoice

from app.handlers.help import send_help_message
from app.handlers.invoice.create import EXPIRING_DATETIME_FORMAT
from app.handlers.wallet.pay import wallet_pay_flow_handler
from utils.message_handler import message_handler

__all__ = (
    'init_start_handler',
)


async def handle_invoice(context, groups):
    invoice_id = groups[0]

    invoice = await load_invoice(
        context.user,
        context.db_session,
        filters=[
            InvoiceModel.id == int(invoice_id),
        ],
        check_wallet=False,
    )

    if invoice is None or invoice.status != InvoiceStatus.PENDING:
        return await context.send_message('Invalid invoice id')

    if invoice.is_expired():
        return await context.send_message('Invoice expired')

    count = invoice.count
    if invoice.to_wallet.get_currency() == 'BTC':
        count = Decimal(invoice.count) / Decimal(1e8)

    await context.send_message(
        'You will pay: \n'
        'To: %s\n'
        'Count: %s %s\n'
        'Description: %s\n'
        'Expiring in %s' % (
            invoice.to_wallet.address,
            str(count),
            invoice.to_wallet.get_currency(),
            invoice.description,
            invoice.expiring.strftime(EXPIRING_DATETIME_FORMAT),
        )
    )

    async def set_invoice_id(ctx):
        ctx.state.data['invoice_id'] = invoice_id

    await wallet_pay_flow_handler.start(context, prepare=set_invoice_id)


PREFIXES = {
    re.compile('^' + pattern + '$'): handler
    for pattern, handler in [
        ('invoice_id=(\\d+)', handle_invoice),
    ]
}


def init_start_handler():
    @message_handler(
        bot_commands=['start'],
    )
    async def message_start(context):
        await context.clear_state()

        text = await context.get_message_text()
        text = text[7:]

        for pattern, handler in PREFIXES.items():
            search = pattern.search(text)
            if search is not None:
                return await handler(context, search.groups())

        await context.send_message('Welcome to Cracc Wallet Bot')
        await send_help_message(context)
