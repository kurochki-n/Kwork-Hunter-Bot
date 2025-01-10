from typing import List

from aiogram.types import Message
from aiohttp import ClientSession

from sqlalchemy.ext.asyncio import AsyncSession

from api.kwork import KworkAPI
from bot.handlers import localization as loc
from bot.handlers import keyboards as kb
from db.models import User


async def get_admins() -> List[int]:
    """Get admins from the database.

    Returns:
        List[int]: List of admins' ids.
    """
    ...
            
            
async def projects_tracking(user: User, message: Message, db_session: AsyncSession) -> None:
    async with ClientSession() as session:
        kwork = KworkAPI(session)
        kwork.headers["Cookie"] = user.kwork_cookie
        success, projects = await kwork.get_projects()
        if not success:
            return
        
        projects_ids = []
        
        for project in projects:
            projects_ids.append(project.get("id"))
            if project.get("id") not in user.last_projects:
                files = project.get("files")
                await message.answer(
                    text=loc.project_info(project), 
                    reply_markup=kb.project_keyboard(project_id=project["id"], files=files), 
                    disable_web_page_preview=True
                )
                
        user.last_projects = projects_ids
        await db_session.commit()

