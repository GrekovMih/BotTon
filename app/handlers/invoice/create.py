# -*- encoding: utf-8 -*-
from _decimal import Decimal
from datetime import timedelta, datetime

from cracc_database.app.models.invoices import InvoiceModel

from app.handlers.flow_handler import FlowHandler, FlowHandlerStep
from app.handlers.wallet.pay import StepChooseWallet, get_wallet
from utils.keyboard import BotKeyboard

__all__ = (
    'EXPIRING_DATETIME_FORMAT',
    'invoice_create_flow_handler',
)

EXPIRING_VARIANTS = {
    'In 1 hour': timedelta(hours=1),
    'In 1 day': timedelta(days=1),
    'In 1 week': timedelta(weeks=1),
    'Custom date and time': None,
}

EXPIRING_DATETIME_FORMAT = '%d.%m.%y %H:%M:%S'


class StepCount(FlowHandlerStep):
    async def before(self, context):
        await context.send_message('How much BTC you want to receive?')

    async def handle(self, context):
        count = await context.get_message_text()

        try:
            count = Decimal(count)
            assert count > 0

        except:
            await context.send_message('Invalid count')
            return False

        context.state.data['count'] = str(count)
        return True


class StepDescription(FlowHandlerStep):
    async def before(self, context):
        await context.send_message('Enter invoice description:')

    async def handle(self, context):
        description = await context.get_message_text()
        context.state.data['description'] = description
        return True


class StepExpiring(FlowHandlerStep):
    variants_keyboard = BotKeyboard.gef_native(EXPIRING_VARIANTS.keys())

    async def before(self, context):
        await context.send_message(
            'Enter invoice expiring:',
            reply_markup=StepExpiring.variants_keyboard,
        )

    async def handle(self, context):
        text = await context.get_message_text()
        expiring = EXPIRING_VARIANTS.get(text, None)

        if expiring is None:
            try:
                expiring = datetime.strptime(expiring, EXPIRING_DATETIME_FORMAT)

                if expiring < datetime.now():
                    await context.send_message('Invalid value', reply_markup=StepExpiring.variants_keyboard)
                    return False

            except Exception:
                await context.send_message('You can enter datetime in %s format' % EXPIRING_DATETIME_FORMAT)
                return False

        else:
            expiring = datetime.now() + expiring

        context.state.data['expiring'] = str(expiring.timestamp())

        return True


class StepConfirm(FlowHandlerStep):
    async def before(self, context):
        wallet = await get_wallet(context)
        data = context.state.data

        await context.send_message(
            'You want to receive: \n'
            'Address: %s\n'
            'Count: %s %s\n'
            'Description: %s\n'
            'Expiring in %s' % (
                wallet.address,
                data['count'],
                wallet.get_currency(),
                data['description'],
                datetime.fromtimestamp(float(data['expiring'])).strftime(EXPIRING_DATETIME_FORMAT),
            )
        )

        await context.send_message('All right?', reply_markup=BotKeyboard.gef_native(['Yes', 'No']))

    async def handle(self, context):
        text = await context.get_message_text()

        if text == 'No':
            await context.send_message('Restarting')
            await invoice_create_flow_handler.start(context)
            return False

        if text != 'Yes':
            await context.send_message('Invalid value')
            return False

        data = context.state.data
        wallet = await get_wallet(context)

        invoice = InvoiceModel()
        invoice.to_wallet_id = data['wallet_id']
        invoice.count = Decimal(data['count'])
        if wallet.get_currency() == 'BTC':
            invoice.count *= Decimal(1e8)

        invoice.expiring = datetime.fromtimestamp(float(data['expiring']))
        invoice.description = data['description']

        context.db_session.add(invoice)
        context.db_session.commit()
        context.db_session.refresh(invoice)

        await context.send_message(
            'Great! Invoice was created.\n'
            'Link for buyer: https://xxxxx' % invoice.id
        )


invoice_create_flow_handler = FlowHandler(
    'invoice_create',
    [
        StepChooseWallet,
        StepCount,
        StepDescription,
        StepExpiring,
        StepConfirm,
    ],
)
