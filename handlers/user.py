from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext

from data.mysql.database import DataBase
from . import localization as loc, keyboards as kb


router = Router()
db = DataBase()


@router.message(Command("start"))
async def command_handler(message: Message, state: FSMContext):
    await db.check_user_in_database(message.from_user.id)
    await message.answer(text=loc.start_message(message.from_user.first_name), reply_markup=kb.travel_guide_keyboard())

    
@router.message(F.text == "⚙️ Настройки")
async def text_handler(message: Message, state: FSMContext):
    await message.answer(text=loc.selecting_section(), reply_markup=kb.settings_menu_keyboard())
    
    
@router.message(F.text == "👤 Профиль")
async def text_handler(message: Message, state: FSMContext):
    pass
    
    
@router.message(F.text == "ℹ️ Информация")
async def text_handler(message: Message, state: FSMContext):
    pass


@router.callback_query(F.data == "settings")
async def calldack_query_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=loc.selecting_section(), reply_markup=kb.settings_menu_keyboard())


@router.callback_query(F.data == "categories")
async def calldack_query_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=loc.categories(), reply_markup=kb.categories_keyboard())


@router.callback_query(F.data == "notifications")
async def calldack_query_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(text=loc.notifications(), reply_markup=kb.notifications_keyboard(callback.from_user.id))
    

    






