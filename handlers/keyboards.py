from aiogram import types
from aiogram.types.web_app_info import WebAppInfo


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

def categories_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text='Дизайн', callback_data='design')],
        [types.InlineKeyboardButton(text='Разработка и IT', callback_data='development-it')],
        [types.InlineKeyboardButton(text='Тексты и переводы', callback_data='texts-ranslations')],
        [types.InlineKeyboardButton(text='SEO и трафик', callback_data='seo-traffic')],
        [types.InlineKeyboardButton(text='Соцсети и реклама', callback_data='socialmedia-advertising')],
        [types.InlineKeyboardButton(text='Аудио, видео, съемка', callback_data='audio-video-shooting')],
        [types.InlineKeyboardButton(text='Бизнес и жизнь', callback_data='business-life')],
        [types.InlineKeyboardButton(text='🔙 Назад', callback_data='settings')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    return keyboard
