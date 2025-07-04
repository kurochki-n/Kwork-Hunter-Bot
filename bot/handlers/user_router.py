from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import selectinload 
from sqlalchemy.ext.asyncio import AsyncSession

from . import localization as loc, keyboards as kb
from .states import States
from api import KworkAPI
from api.kwork import auth
from db import User
from bot.utils import scheduler_func
from cryptographer import encrypt, decrypt


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, db_session: AsyncSession) -> None:
    await message.answer(text=loc.start_message(message.from_user.first_name), reply_markup=kb.main_keyboard())
    
    user = await db_session.scalar(
        select(User)
        .options(selectinload(User.kwork_session))
        .where(User.id == message.from_user.id)
    )
    
    if not user.kwork_session.login:
        await message.answer(text=loc.auth(), reply_markup=kb.auth_keyboard())
    

@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message, db_session: AsyncSession) -> None:
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    user = await db_session.scalar(
        select(User)
        .options(selectinload(User.kwork_session))
        .where(User.id == user_id)
    )
        
    await message.answer(text=loc.user_profile(first_name, user_id), reply_markup=kb.profile_keyboard(user))


@router.message(F.text == "💬 Помощь")
async def help_handler(message: Message) -> None:
    await message.answer(text=loc.help_sections(), reply_markup=kb.help_keyboard())
    
    
@router.callback_query(F.data == "enable_tracking")
async def enable_projects_tracking_handler(callback: CallbackQuery, db_session: AsyncSession, scheduler: AsyncIOScheduler) -> None:
    user = await db_session.scalar(
        select(User)
        .options(selectinload(User.kwork_session))
        .where(User.id == callback.from_user.id)
    )
    
    if not user.kwork_session.login:
        message = await callback.message.answer(
            text=loc.enter_kwork_login(), 
            reply_markup=kb.log_in_keyboard(
                message_id=None
            )
        )
        await message.edit_reply_markup(reply_markup=kb.log_in_keyboard(message_id=message.message_id))
        return
    
    async with ClientSession() as session:
        kwork = KworkAPI(session)
        success, cookie, _ = await kwork.login(decrypt(user.kwork_session.login), decrypt(user.kwork_session.password))
        
        if not success:
            await callback.message.answer(text=loc.error_auth(), reply_markup=kb.auth_keyboard())
            return
        
        cookie_str = '; '.join([f"{key}={morsel.value}" for key, morsel in cookie.items()])
        user.kwork_session.cookie = encrypt(cookie_str)
        await db_session.commit()
        
        job_id = str(user.id)
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            
        scheduler.add_job(
            func=scheduler_func.projects_tracking, 
            id=job_id, 
            trigger="interval", 
            minutes=1, 
            kwargs={
                "user": user, 
                "message": callback.message, 
                "db_session": db_session
            }
        )
        
        await callback.message.edit_reply_markup(reply_markup=kb.profile_keyboard(user))
        await callback.answer(text=loc.projects_tracking_enabled())
        
        
@router.callback_query(F.data == "disable_tracking")
async def disable_projects_tracking_handler(callback: CallbackQuery, db_session: AsyncSession, scheduler: AsyncIOScheduler) -> None:
    user = await db_session.scalar(
        select(User)
        .options(selectinload(User.kwork_session))
        .where(User.id == callback.from_user.id)
    )
    
    try:
        scheduler.remove_job(str(user.id))
    finally:
        user.kwork_session.cookie = None
        await db_session.commit()
        
        await callback.message.edit_reply_markup(reply_markup=kb.profile_keyboard(user))
        await callback.answer(text=loc.projects_tracking_disabled())
    
    
@router.callback_query(F.data == "manual")
async def manual_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text=loc.manual(), reply_markup=kb.help_back_keyboard())
    
    
@router.callback_query(F.data == "support")
async def support_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text=loc.support(), reply_markup=kb.help_back_keyboard())
    
    
@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text=loc.help_sections(), reply_markup=kb.help_keyboard())


@router.callback_query(F.data == "hide_project")
async def hide_project_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == "auth")
async def auth_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer(text=loc.get_login(), reply_markup=kb.cancel_keyboard())
    await state.set_state(States.get_login)
    

@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=loc.canceled(), reply_markup=kb.main_keyboard())
    await state.clear()
    

@router.message(StateFilter(States.get_login))
async def get_login_handler(message: Message, state: FSMContext) -> None:
    await state.set_data({"login": message.text})
    await message.answer(text=loc.get_password(), reply_markup=kb.cancel_keyboard())
    await state.set_state(States.get_password)
    

@router.message(StateFilter(States.get_password))
async def get_password_handler(message: Message, state: FSMContext, db_session: AsyncSession) -> None:
    data = await state.get_data()
    await state.clear()
    
    login = data['login']
    password = message.text
    
    success, err = await auth(login, password, message.from_user.id, db_session)
    if not success:
        await message.answer(text=loc.error_auth(err), reply_markup=kb.auth_keyboard())
        return
    
    await message.answer(text=loc.successful_auth(), reply_markup=kb.main_keyboard())