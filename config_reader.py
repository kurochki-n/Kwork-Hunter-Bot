from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from tuna_manager import start_tuna

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    CHANNEL_ID: SecretStr
    DB_URL: SecretStr
    
    WEBAPP_PORT: Optional[int] = None
    WEBHOOK_PORT: Optional[int] = None

    WEBAPP_URL: Optional[SecretStr] = None
    WEBAPP_PID: Optional[int] = None
    WEBHOOK_URL: Optional[SecretStr] = None
    WEBHOOK_PID: Optional[int] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        webapp_url, webapp_pid = start_tuna(self.WEBAPP_PORT, 'kworkhunter-webapp')
        webhook_url, webhook_pid = start_tuna(self.WEBHOOK_PORT, 'kworkhunter-webhook')
        
        if webapp_url and webhook_url:
            self.WEBAPP_URL = SecretStr(webapp_url)
            self.WEBAPP_PID = webapp_pid
            self.WEBHOOK_URL = SecretStr(webhook_url)
            self.WEBHOOK_PID = webhook_pid
        else:
            raise Exception("Couldn't get URL from tuna")


config = Config()



