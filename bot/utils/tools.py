import os
import aiofiles

from typing import List

from aiogram.types import Message, FSInputFile
from aiohttp import ClientSession

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.kwork import KworkAPI
from bot.handlers import localization as loc
from bot.handlers import keyboards as kb
from db.models import User
from utils.cryptographer import decrypt


async def get_admins(db_session: AsyncSession) -> List[int]:
    """Get admins from the database.

    Returns:
        List[int]: List of admins' ids.
    """
    return await db_session.scalars(select(User).where(User.is_admin == True))
            
            
async def projects_tracking(user: User, message: Message, db_session: AsyncSession) -> None:
    async with ClientSession() as session:
        kwork = KworkAPI(session)
        kwork.headers["Cookie"] = decrypt(user.kwork_session.cookie)
        success, projects = await kwork.get_projects()
        if not success:
            return
        
        projects_ids = []
        
        for project in projects:
            projects_ids.append(project.get("id"))
            if project.get("id") not in user.kwork_session.last_projects:
                for file in project.get("files"):
                    content = await kwork.get_file_content(url=file["url"])
                    os.makedirs("temp", exist_ok=True)
                    filepath = f"temp/{file['fname']}"
                    
                    async with aiofiles.open(filepath, "wb") as file:
                        await file.write(content)
                    
                    await message.answer_document(
                        document=FSInputFile(filepath)
                    )
                    os.remove(filepath)
                await message.answer(
                    text=loc.project_info(project), 
                    reply_markup=kb.project_keyboard(project_id=project["id"]), 
                    disable_web_page_preview=True
                )
                
        user.kwork_session.last_projects = projects_ids
        await db_session.commit()

