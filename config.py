from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Telegram Bot Token
    BOT_TOKEN: str
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///rentacar.db"
    
    class Config:
        env_file = ".env"

settings = Settings()