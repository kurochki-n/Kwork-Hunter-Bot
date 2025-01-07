import re
from typing import Dict, Any

from db import User


def remove_emojis(text: str) -> str:
    """Remove emojis from the text.

    Args:
        text (str): Text to remove emojis from.

    Returns:
        str: Text without emojis.
    """
    lines = text.split('\n')
    cleaned_lines = [re.sub(r'\s*\[:\w+-?\w*\]\s*', ' ', line).strip() for line in lines]
    return '\n'.join(cleaned_lines)


def start_message(username: str | None) -> str:
    if username is None: username = "пользователь"
    return f"👋 <b>Привет, {username}!\n\n" \
           "🔸 Я помогу тебе следить за проектами на бирже Kwork и откликаться на них быстрее остальных!\n" \
           "🔸 Это увеличит шансы на то, что заказчик выберет именно тебя!\n\n" \
           "🚀 Чтобы начать, перейди в раздел «Профиль» и включи отслеживание проектов.</b>\n"
           
           
def no_sub() -> str:
    return "<b>📣 Для использования бота необходимо подписаться на наш канал.</b>"


def project_info(data: Dict[str, Any]) -> str:
    username = data['wantUserGetProfileUrl'].split('/')[-1]
    profile_url = f"https://kwork.ru/user/{username}"
    projects_url = f"https://kwork.ru/projects/list/{username}"
    
    cleaned_name = remove_emojis(data['name'])
    cleaned_description = remove_emojis(data['description'])
    
    return f"<blockquote><b>{cleaned_name}</b>\n\n" \
           f"{cleaned_description.replace('\n', '\n\n')}</blockquote>\n\n" \
           f"Желаемый бюджет: до {int(float(data['priceLimit']))} ₽\n" \
           f"Допустимый: до {int(float(data['possiblePriceLimit']))} ₽\n\n" \
           f"Покупатель: <a href='{profile_url}'>{username}</a>\n" \
           f"Размещено проектов на бирже: {data['user']['data']['wants_count']}   " \
           f"<a href='{projects_url}'>Смотреть открытые ({data['getWantsActiveCount']})</a>\n" \
           f"Нанято: {data['user']['data']['wants_hired_percent']}%\n\n" \
           f"Осталось: {data['timeLeft']}\n" \
           f"Предложений: {data['kwork_count']}"
           
           
def user_profile(user: User) -> str:
    return f"<b><code>{user.id}</code></b>"
    
            
def enter_kwork_login() -> str:
    return "<b>📲 Войди в свой аккаунт Kwork, чтобы бот мог отслеживать проекты по твоим любимым категориям.</b>"


def error_login() -> str:
    return "<b>⚠️ Произошла ошибка при входе в Kwork. Введи логин и пароль еще раз.</b>"


def projects_tracking_enabled() -> str:
    return "🔔 Отслеживание проектов включено"


def projects_tracking_disabled() -> str:
    return "🔕 Отслеживание проектов выключено"


def temp_message(seconds: int) -> str:
    return f"<b>✅ Авторизация прошла успешно!</b>\n\n<i>Сообщение будет удалено через {seconds} секунд...</i>"





