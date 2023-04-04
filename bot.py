# -*- encoding: utf-8 -*-
import telebot
from telebot import apihelper

import settings

__all__ = (
    'bot',
)

apihelper.proxy = {'https':settings.TELEBOT_PROXY}


bot = telebot.TeleBot(settings.BOT_TOKEN)