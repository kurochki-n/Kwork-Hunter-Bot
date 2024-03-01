import aiohttp

from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

from api.parser import KworkParser


def settings_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text='📊 Категории', callback_data='categories')],
        [types.InlineKeyboardButton(text='📬 Уведомления', callback_data='notifications')]
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

async def categories_keyboard():
    async with aiohttp.ClientSession() as session:
        buttons = []
        parser = KworkParser(session=session)
        categories = await parser.get_categories()
        
        for cat in categories:
            buttons.append([types.InlineKeyboardButton(text=f'{cat}', callback_data=f'{cat}')])
        buttons.append([types.InlineKeyboardButton(text='🔙 Назад', callback_data='settings')])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
        return keyboard
