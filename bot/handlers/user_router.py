from aiohttp import ClientSession

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import localization as loc, keyboards as kb
from bot.middlewares.channel_sub import CheckSubscription
from api.kwork import KworkAPI
from db import User
from bot.utils import tools
from utils.cryptographer import encrypt, decrypt

router = Router()
router.message.middleware.register(CheckSubscription())
router.callback_query.middleware.register(CheckSubscription())


@router.message(CommandStart())
async def start(message: Message, db_session: AsyncSession) -> None:
    await message.answer(text=loc.start_message(message.from_user.username), reply_markup=kb.main_keyboard())
    
    user = await db_session.scalar(select(User).where(User.id == message.from_user.id))
    if not user.kwork_login:
        msg = await message.answer(
            text=loc.enter_kwork_login(), 
            reply_markup=kb.log_in_keyboard(
                message_id=None
            )
        )
        await msg.edit_reply_markup(reply_markup=kb.log_in_keyboard(message_id=msg.message_id))
    
    
@router.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery) -> None:
    await callback.message.answer(text=loc.start_message(callback.from_user.username), reply_markup=kb.main_keyboard())
    await callback.answer()
    
    
@router.message(F.text == "👤 Профиль")
async def profile(message: Message, db_session: AsyncSession) -> None:
    user = await db_session.scalar(select(User).where(User.id == message.from_user.id))
    await message.answer(text=loc.user_profile(user, message.from_user.username), reply_markup=kb.profile_keyboard(user))
    
    
@router.message(F.text == "💬 Помощь")
async def help(message: Message, state: FSMContext, db_session: AsyncSession) -> None:
    await message.answer(text=loc.help_sections(), reply_markup=kb.help_keyboard())
    
    
@router.callback_query(F.data == "enable_tracking")
async def enable_projects_tracking(callback: CallbackQuery, db_session: AsyncSession, scheduler: AsyncIOScheduler) -> None:
    user = await db_session.scalar(select(User).where(User.id == callback.from_user.id))
    
    if not user.kwork_login:
        message = await callback.message.answer(
            text=loc.enter_kwork_login(), 
            reply_markup=kb.log_in_keyboard(
                message_id=None
            )
        )
        await message.edit_reply_markup(reply_markup=kb.log_in_keyboard(message_id=message.message_id))
        await callback.answer()
        return
    
    async with ClientSession() as session:
        kwork = KworkAPI(session)
        success, cookie, _ = await kwork.login(decrypt(user.kwork_login), decrypt(user.kwork_password))
        
        if not success:
            message = await callback.message.answer(
                text=loc.error_login(), 
                reply_markup=kb.log_in_keyboard(
                    message_id=None
                )
            )
            await message.edit_reply_markup(reply_markup=kb.log_in_keyboard(message_id=message.message_id))
            await callback.answer()
            return
        
        cookie_str = '; '.join([f"{key}={morsel.value}" for key, morsel in cookie.items()])
        user.kwork_cookie = encrypt(cookie_str)
        await db_session.commit()
        
        scheduler.add_job(
            func=tools.projects_tracking, 
            id=str(user.id), 
            trigger="interval", 
            minutes=2, 
            kwargs={
                "user": user, 
                "message": callback.message, 
                "db_session": db_session
            }
        )
        
        await callback.message.edit_reply_markup(reply_markup=kb.profile_keyboard(user))
        await callback.answer(text=loc.projects_tracking_enabled())
        
        
@router.callback_query(F.data == "disable_tracking")
async def disable_projects_tracking(callback: CallbackQuery, db_session: AsyncSession, scheduler: AsyncIOScheduler) -> None:
    user = await db_session.scalar(select(User).where(User.id == callback.from_user.id))
    
    scheduler.remove_job(str(user.id))
    
    user.kwork_cookie = None
    await db_session.commit()
    
    await callback.message.edit_reply_markup(reply_markup=kb.profile_keyboard(user))
    await callback.answer(text=loc.projects_tracking_disabled())
    
    
@router.callback_query(F.data == "manual")
async def manual(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text=loc.manual(), reply_markup=kb.help_back_keyboard())
    
    
@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text=loc.support(), reply_markup=kb.help_back_keyboard())
    
    
@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text=loc.help_sections(), reply_markup=kb.help_keyboard())


@router.callback_query(F.data == "hide_project")
async def hide_project(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
















