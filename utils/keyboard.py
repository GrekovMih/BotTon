# -*- encoding: utf-8 -*-
import telebot

__all__ = (
    'BotKeyboard',
)


def add_rows(keyboard, rows):
    for row in rows:
        if type(row) is tuple:
            keyboard.row(*row)
        else:
            keyboard.row(row)

    return keyboard


class BotKeyboard:
    InlineButton = telebot.types.InlineKeyboardButton

    @staticmethod
    def gef_native(rows, resize_keyboard=True, one_time_keyboard=True, *args, **kwargs):
        keyboard = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            *args,
            **kwargs,
        )

        add_rows(keyboard, rows)

        return keyboard

    @staticmethod
    def get_inline(rows, *args, **kwargs):
        keyboard = telebot.types.InlineKeyboardMarkup(*args, **kwargs)

        add_rows(keyboard, rows)

        return keyboard

    @staticmethod
    def remove():
        return telebot.types.ReplyKeyboardRemove()
