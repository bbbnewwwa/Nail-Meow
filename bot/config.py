from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Вставь свой токен от @BotFather!
    API_URL: str = "http://127.0.0.1:8000/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()