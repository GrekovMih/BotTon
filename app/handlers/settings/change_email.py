import re
from uuid import uuid4

from app.handlers.flow_handler import FlowHandler, FlowHandlerStep
from cracc_database.app.models.users import UserStatus
from cracc_mail.services import send_bot_change_email, send_registration_success

__all__ = (
    'settings_change_email_flow_handler',
)


class StepCurrency(FlowHandlerStep):
    async def before(self, context):
        await context.send_message('Input your email')

    async def handle(self, context):

        context.state.data['tg_mail'] = await context.get_message_text()
        pattern = re.compile('(^|\s)[-a-zA-Z0-9_.]+@([-a-zA-Z0-9]+\.)+[a-zA-Z]{2,6}(\s|$)')
        is_valid = pattern.match(context.state.data['tg_mail'])

        if is_valid:

            user = context.user
            old_email = user.email
            user.email = context.state.data['tg_mail']

            token = str(uuid4())
            await send_bot_change_email(user, token)
            context.state.data['token'] = token
            user.email = old_email

            await context.send_message('Please, check the mail. The token will be in the letter.')

            return True


        else:
            await context.send_message('Not valid email')
            return False


class StepToken(FlowHandlerStep):
    async def before(self, context):
        await context.send_message('Enter token from mail:')

    async def handle(self, context):
        token = await context.get_message_text()
        if (context.state.data['token'] == token):

            context.user.status = UserStatus.VERIFIED

            context.user.email = context.state.data['tg_mail']

            await context.send_message('Email was VERIFIED')
            await send_registration_success(context.user)
            return True


        else:

            await context.send_message('Token is wrong')
            return False


settings_change_email_flow_handler = FlowHandler(
    'settings_change_email',
    [
        StepCurrency,
        StepToken
    ],
)
