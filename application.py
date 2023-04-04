# -*- encoding: utf-8 -*-
import subprocess

import sentry_sdk
import settings

from app.handlers import init_handlers
from bot import bot

if __name__ == '__main__':
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN_API,
        release=subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8'),
        # integrations=[SanicIntegration()], # need to migrate all to python 3.7
    )


    init_handlers()

    bot.polling(none_stop=True)
