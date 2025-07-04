from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from db import User


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="💬 Помощь")]
    ], resize_keyboard=True)


def project_keyboard(project_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text="Открыть проект", 
            url=f"https://kwork.ru/projects/{project_id}/view"
        )],
        [InlineKeyboardButton(
            text="Предложить услугу", 
            url=f"https://kwork.ru/new_offer?project={project_id}"
        )],
        [InlineKeyboardButton(
            text="🗑 Скрыть", 
            callback_data=f"hide_project"
        )],
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
    
    
def profile_keyboard(user: User) -> InlineKeyboardMarkup:
    buttons = []
    if user.kwork_session.cookie:
        buttons.append([InlineKeyboardButton(text="Выключить отслеживание проектов", callback_data="disable_tracking")])
    else:
        buttons.append([InlineKeyboardButton(text="Включить отслеживание проектов", callback_data="enable_tracking")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
    
    
def help_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Инструкция", callback_data="manual")],
        [InlineKeyboardButton(text="👨‍👩‍👦‍👦 Поддержка", callback_data="support")]
    ])
    
    
def help_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])
    
    
def auth_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Авторизоваться", callback_data="auth")]
    ])
    
    
def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ])