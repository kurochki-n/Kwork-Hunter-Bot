import os
import json

import aiofiles
from aiogram.types import Message, FSInputFile
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from api import KworkAPI
from bot.handlers import localization as loc
from bot.handlers import keyboards as kb
from db.models import User
from cryptographer import decrypt
            
            
async def projects_tracking(user: User, message: Message, db_session: AsyncSession) -> None:
    """
    Tracks new projects for the user on Kwork and sends information about them to the chat.

    Args:
        user (User): The user object for whom the project tracking is performed.
        message (Message): The message object used to send information to the user.
        db_session (AsyncSession): The asynchronous session for database operations.

    Returns:
        None
    """
    async with ClientSession() as session:
        kwork = KworkAPI(session)
        kwork.headers["Cookie"] = decrypt(user.kwork_session.cookie)
        success, projects = await kwork.get_projects()
        
        if not success:
            return
        
        projects_ids = []
        
        for project in projects:
            attachment = False
            projects_ids.append(project.get("id"))
            
            if project.get("id") not in json.loads(user.kwork_session.last_projects):
                for file in project.get("files"):
                    content = await kwork.get_file_content(url=file["url"])
                    filepath = f"temp/{file['fname']}"
                    
                    async with aiofiles.open(filepath, "wb") as file:
                        await file.write(content)
                    
                    await message.answer_document(
                        document=FSInputFile(filepath),
                        caption=loc.remove_emojis(project['name'])
                    )
                    os.remove(filepath)
                    attachment = True
                    
                await message.answer(
                    text=loc.project_info(project, attachment), 
                    reply_markup=kb.project_keyboard(project_id=project["id"]), 
                    disable_web_page_preview=True
                )
                
        user.kwork_session.last_projects = json.dumps(projects_ids)
        await db_session.commit()
