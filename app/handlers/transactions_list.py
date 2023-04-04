# -*- encoding: utf-8 -*-
from app.handlers.flow_handler import FlowHandler, FlowHandlerStep
from app.services.wallets import get_transactions
from app.wallets import get_wallets_list
from utils.keyboard import BotKeyboard

__all__ = (
    'transactions_list_flow_handler',
)


async def get_count(count, wallet):
    return str(count) + ' ' + wallet.get_currency()


async def send_transactions_list(context):
    wallets = await get_wallets_list(context)
    wallets = {
        wallet.id: wallet
        for wallet in wallets
    }

    page = context.state.data.get('page', 1)
    transactions = await get_transactions(context.user.id, count=5, page=page)

    msg = ''.join([
        'Date: %s\n'
        'Hash: %s\n'
        'To: %s\n'
        'Count: %s\n'
        'Fee: %s\n'
        '\n' % (
            tx['created_at'],
            tx['hash'],
            tx['to'],
            await get_count(tx['count'], wallets[tx['wallet']['id']]),
            await get_count(tx['fee'], wallets[tx['wallet']['id']]),
        )
        for tx in transactions
    ])

    return await context.send_message(msg, reply_markup=BotKeyboard.gef_native(['Еще']))


class StepTransactionsList(FlowHandlerStep):
    async def before(self, context):
        await send_transactions_list(context)

    async def handle(self, context):
        context.state.data['page'] = context.state.data.get('page', 1) + 1
        await send_transactions_list(context)
        return False


transactions_list_flow_handler = FlowHandler(
    'transactions_list',
    [
        StepTransactionsList,
    ],
)
