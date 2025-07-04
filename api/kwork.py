import logging
import traceback
from typing import Dict, Any, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from http.cookies import SimpleCookie

from db import User
from cryptographer import encrypt


async def auth(login: str, password: str, user_id: int, db_session: AsyncSession) -> Tuple[bool, Optional[str]]:
    try:
        logging.info(f"Starting auth process for user_id: {user_id}")
        async with ClientSession() as session:
            kwork = KworkAPI(session)
            logging.info("Attempting Kwork login")
            success, _, response_data = await kwork.login(login, password)
            
            if not success:
                error_message = response_data.get('error') if response_data else "Неизвестная ошибка"
                logging.error(f"Kwork login failed: {error_message}")
                return False, error_message
            
            logging.info("Kwork login successful, updating database")
            user = await db_session.scalar(
                select(User)
                .options(selectinload(User.kwork_session))
                .where(User.id == user_id)
            )
            user.kwork_session.login = encrypt(login)
            user.kwork_session.password = encrypt(password)
            await db_session.commit()
            
            return True, None
        
    except Exception as e:
        logging.error(f"Auth error: {str(e)}\n{traceback.format_exc()}")
        await db_session.rollback()
        return False, "Неизвестная ошибка"


class KworkAPI(object):
    
    def __init__(self, session: ClientSession) -> None:
        self.session = session
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "kwork.ru",
            "Origin": "https://kwork.ru",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }
        
    async def login(self, username: str, password: str) -> Tuple[bool, Optional[SimpleCookie], Optional[Dict[str, Any]]]:
        """Login to Kwork.

        Args:
            username (str): Kwork username
            password (str): Kwork password

        Returns:
            Tuple[bool, SimpleCookie, Dict[str, Any] | None]: Success, cookie, login response.
        """
        url = "https://kwork.ru/api/user/login"
        body = {
            "l_username": username,
            "l_password": password,
            "jlog": 1,
            "recaptcha_pass_token": "",
            "g-recaptcha-response": "",
            "track_client_id": False,
            "l_remember_me": "1"
        }
        
        async with self.session.post(url, headers=self.headers, json=body) as response:
            if response.status == 200:
                response_data = await response.json()
                if response_data["success"]:
                    return True, response.cookies, response_data
                else:
                    logging.error(f"Login failed with error: {response_data['error']}")
                    return False, None, response_data
            else:
                logging.error(f"Login failed with status code: {response.status}")
                return False, None, None

    async def get_projects(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Get projects.

        Returns:
            Tuple[Dict[str, Any] | None, bool]: Projects, success.
        """
        url = "https://kwork.ru/projects?a=1&page=1"
        body = self.create_body(a=1)
        projects = []

        async with self.session.post(url, headers=self.headers, data=body) as response:
            if response.status == 200:
                response_data = await response.json()
                if response_data["success"]:
                    projects.extend(response_data["data"]["pagination"]["data"])
                else:
                    logging.error(f"Failed to get projects with error: {response_data['error']}")
                    return False, None
            else:
                logging.error(f"Failed to get projects with status code: {response.status}")
                return False, None
            
        return True, projects
    
    def create_body(self, **kwargs) -> str:
        """Create the request body.

        Args:
            **kwargs: Keyword arguments.

        Returns:
            str: Body.
        """
        body = ""
        for key, value in kwargs.items():
            body += f"------WebKitFormBoundary\nContent-Disposition: form-data; name='{key}'\n\n{value}\n"
        body += "-----WebKitFormBoundary--"
        return body
            
    async def get_file_content(self, url: str) -> bytes:
        async with self.session.get(url, headers=self.headers) as response:
            return await response.content.read()
            