from aiogram import types
from aiogram.types.web_app_info import WebAppInfo


def inline_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text='text', callback_data='data'),
            types.InlineKeyboardButton(text='text1', callback_data='data1')
        ],
        [types.InlineKeyboardButton(text='text2', callback_data='data2')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard

def travel_guide_keyboard():
    buttons = [
        [types.KeyboardButton(text='⚙️ Настройки')],
        [types.KeyboardButton(text='👤 Профиль')],
        [types.KeyboardButton(text='ℹ️ Информация')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def inline_webapp_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text='text', web_app=WebAppInfo(url='url'))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard
