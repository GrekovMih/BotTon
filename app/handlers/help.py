# -*- encoding: utf-8 -*-

__all__ = (
    'send_help_message',
)


async def send_help_message(context):
    await context.send_message(
        disable_web_page_preview=True,
        parse_mode='Markdown',
        text='I can help you create and manage Cracc wallets.\n\n'
             'You can control me by sending these commands:\n'
             '\n'
             '/wallets - Wallets list\n'
             '/wallet\_create - Create wallet\n'
             '/wallet\_pay - Pay from wallet\n'
             '\n'
             '/transactions - Transactions list\n'
             '\n'
             '/invoice\_create - Create invoice\n'
             '\n'
             '/change\_email - Change your email \n'
             '\n'
             '/help - Show this helper\n'
             '\n'
             'For other questions - @akuroglo',
    )
