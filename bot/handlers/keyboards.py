from typing import List, Dict, Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from db import User
from config_reader import config


def start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Помощь")]
    ], resize_keyboard=True)


def project_keyboard(
    project_id: int,
    files: List[Dict[str, Any]] = None,
) -> InlineKeyboardMarkup:
    buttons = []
    
    if files:
        for file in files:
            buttons.append([
                InlineKeyboardButton(
                    text=f"📎 {file['fname']}", 
                    web_app=WebAppInfo(url=file["url"])
                )
            ])
    buttons.extend([
        [InlineKeyboardButton(
            text="Открыть проект", 
            web_app=WebAppInfo(url=f"https://kwork.ru/projects/{project_id}/view")
        )],
        [InlineKeyboardButton(
            text="Предложить услугу", 
            web_app=WebAppInfo(url=f"https://kwork.ru/new_offer?project={project_id}")
        )]
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def channel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url="https://t.me/kwork_hunter")],
        [InlineKeyboardButton(text="Я подписался", callback_data="check_sub")]
    ])
    
    
def profile_keyboard(user: User) -> InlineKeyboardMarkup:
    buttons = []
    if user.kwork_cookie:
        buttons.append([InlineKeyboardButton(text="Выключить отслеживание проектов", callback_data="disable_tracking")])
    else:
        buttons.append([InlineKeyboardButton(text="Включить отслеживание проектов", callback_data="enable_tracking")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def log_in_keyboard(message_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Войти в Kwork",
            web_app=WebAppInfo(url=f"{config.WEBAPP_URL.get_secret_value()}?message_id={message_id}")
        )]
    ])
