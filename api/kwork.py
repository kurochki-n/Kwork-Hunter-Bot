import logging

from typing import Dict, Any, Tuple

from aiohttp import ClientSession
from http.cookies import SimpleCookie


class KworkAPI(object):
    
    def __init__(self, session: ClientSession):
        self.session = session
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "kwork.ru",
            "Origin": "https://kwork.ru",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }
        
        
    async def login(self, username: str, password: str) -> Tuple[bool, SimpleCookie, Dict[str, Any] | None]:
        """Login to Kwork.

        Args:
            username (str): Kwork username
            password (str): Kwork password

        Returns:
            Tuple[Dict[str, Any] | None, bool]: Login response, success.
            {
                "success": bool,
                "error": str,
                "redirect": str,
                "action_after": str,
                "isUserVerified": bool,
                "csrftoken": str
            }
        """
        url = "https://kwork.ru/api/user/login"
        data = {
            "l_username": username,
            "l_password": password,
            "jlog": 1,
            "recaptcha_pass_token": "",
            "g-recaptcha-response": "",
            "track_client_id": False,
            "l_remember_me": "1"
        }
        
        try:
            async with self.session.post(url, headers=self.headers, data=data) as response:
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
        except Exception as e:
            logging.error(f"Login request failed with error: {str(e)}")
            return False, None, None


    async def get_projects(self) -> Tuple[bool, Dict[str, Any] | None]:
        """Get projects.

        Returns:
            Tuple[Dict[str, Any] | None, bool]: Projects, success.
        """
        url = self.create_projects_url()
        body = self.create_body(a=1)
        projects = []
        projects_count = 0
        
        async with self.session.post(url, headers=self.headers, data=body) as response:
            if response.status == 200:
                response_data = await response.json()
                if response_data["success"]:
                    attributes_count = response_data["data"]["attributesCount"]
                    for _, count in attributes_count.items():
                        projects_count += int(count)
                    projects.extend(response_data["data"]["pagination"]["data"])
                else:
                    logging.error(f"Failed to get projects with error: {response_data['error']}")
                    return False, None
            else:
                logging.error(f"Failed to get projects with status code: {response.status}")
                return False, None
            
        pages_count = projects_count // 12 + 1 if projects_count % 12 != 0 else projects_count // 12
        for page in range(2, pages_count + 1):
            url = self.create_projects_url(page)
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


    def create_projects_url(self, page: int = 1) -> str:
        """Create projects url.

        Args:
            page (int, optional): Page number. Defaults to 1.

        Returns:
            str: Projects url.
        """
        return f"https://kwork.ru/projects?a=1&page={page}"
    
    
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
    
    
    async def create_offer(
        self, 
        project_id: int, 
        description: str, 
        kwork_duration: int, 
        kwork_price: int, 
        kwork_name: str
    ) -> bool:
        """Create offer.

        Args:
            project_id (int): Project id.
            description (str): Offer description.
            kwork_duration (int): Offer duration.
            kwork_price (int): Offer price.
            kwork_name (str): Offer name.

        Returns:
            bool: Success.
        """
        url = "https://kwork.ru/api/offer/createoffer"
        body = self.create_body(
            wantId=project_id, 
            offerType="custom", 
            description=description, 
            kwork_duration=kwork_duration, 
            kwork_price=kwork_price, 
            kwork_name=f"<div>{kwork_name}</div>"
        )
        
        async with self.session.post(url, headers=self.headers, data=body) as response:
            if response.status == 200:
                response_data = await response.json()
                if response_data["success"]:
                    return True
                else:
                    logging.error(f"Failed to create offer with error: {response_data['data']['error']}")
                    return False
            else:
                logging.error(f"Failed to create offer with status code: {response.status}")
                return False
