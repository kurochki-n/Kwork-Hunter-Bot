import asyncio
import logging

from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from sqlalchemy import select

from db import User
from core import _sessionmaker, bot
from api.kwork import KworkAPI
from bot.handlers import localization as loc
from config_reader import config


router = APIRouter()
    

@router.post("/auth")
async def auth(
    login: str = Body(...),
    password: str = Body(...),
    user_id: int = Body(...),
    message_id: int = Body(...)
) -> JSONResponse:
    async with _sessionmaker() as db_session:
        try:
            logging.info(f"Starting auth process for user_id: {user_id}")
            connector = ProxyConnector.from_url(config.PROXY_URL.get_secret_value())
            async with ClientSession(connector=connector) as session:
                kwork = KworkAPI(session)
                logging.info("Attempting Kwork login")
                success, _, response_data = await kwork.login(login, password)
                
                if not success:
                    error_message = response_data.get('error') if response_data else "Неизвестная ошибка"
                    logging.error(f"Kwork login failed: {error_message}")
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False, 
                            "message": f"Kwork: {error_message}"
                        }
                    )
                
                logging.info("Kwork login successful, updating database")
                user = await db_session.scalar(select(User).where(User.id == user_id))
                if not user:
                    logging.error(f"User not found in database: {user_id}")
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "message": "Пользователь не найден"
                        }
                    )
                    
                user.kwork_login = login
                user.kwork_password = password
                await db_session.commit()
                
                try:
                    await bot.delete_message(
                        chat_id=user_id, 
                        message_id=message_id
                    )
                    asyncio.create_task(handle_temp_message(user_id))
                except Exception as e:
                    logging.error(f"Error deleting message: {e}")
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "ok": True, 
                        "message": "Данные успешно сохранены"
                    }
                )
        except Exception as e:
            logging.error(f"Auth error: {str(e)}", exc_info=True)
            await db_session.rollback()
            return JSONResponse(
                status_code=500,
                content={
                    "ok": False, 
                    "message": "Произошла ошибка при обработке запроса"
                }
            )
        
        
async def handle_temp_message(user_id: int):
    temp_message = await bot.send_message(
        chat_id=user_id, 
        text=loc.temp_message(seconds=5)
    )
    await asyncio.sleep(1)
    
    for i in range(4, 0, -1):
        await temp_message.edit_text(
            text=loc.temp_message(seconds=i)
        )
        await asyncio.sleep(1)
    
    await bot.delete_message(
        chat_id=user_id, 
        message_id=temp_message.message_id
    )