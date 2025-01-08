import asyncio
import aiohttp
import logging

from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import JSONResponse

from sqlalchemy import select

from db import User
from core import _sessionmaker, bot
from api.kwork import KworkAPI
from bot.handlers import localization as loc


router = APIRouter()
    

@router.post("/auth")
async def auth(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    user_id: int = Query(...),
    message_id: int = Query(...)
) -> JSONResponse:
    async with _sessionmaker() as db_session:
        try:
            async with aiohttp.ClientSession() as session:
                kwork = KworkAPI(session)
                success, _, response_data = await kwork.login(login, password)
                
                if not success:
                    if response_data:
                        return JSONResponse(
                            status_code=400,
                            content={
                                "ok": False, 
                                "message": f"Kwork: {response_data['error']}"
                            }
                        )
                    
                    return JSONResponse(
                        status_code=500,
                        content={
                            "ok": False, 
                            "message": "Произошла ошибка... Не волнуйтесь, мы уже работаем над этим!"
                        }
                    )
                
            user = await db_session.scalar(select(User).where(User.id == user_id))
                
            user.kwork_login = login
            user.kwork_password = password
            await db_session.commit()
            
            await bot.delete_message(
                chat_id=user_id, 
                message_id=message_id
            )
            asyncio.create_task(handle_temp_message(user_id))
            
            return JSONResponse(
                status_code=200,
                content={
                    "ok": True, 
                    "message": "Данные успешно сохранены"
                }
            )
        except Exception as e:
            await db_session.rollback()
            logging.error(f"Error: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "ok": False, 
                    "message": "Произошла ошибка... Не волнуйтесь, мы уже работаем над этим!"
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