from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import decouple
import pathlib
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()



class BackendConfig(BaseSettings):
    # Server settings
    HOST: str = decouple.config('BACKEND_HOST', cast=str, default='localhost')
    PORT: int = decouple.config('BACKEND_PORT', cast=int, default=8000)
    WORKER: int = decouple.config('BACKEND_WORKER', cast=int, default=1)
    API_PREFIX: str = decouple.config('BACKEND_API_PREFIX', cast=str, default='/api')


    # Middleware settings
    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool, default=True)  # type: ignore
    ALLOWED_ORIGINS: list = ["*"]
    ALLOWED_METHODS: list = ["*"]
    ALLOWED_HEADERS: list = ["*"]

    # Logging settings
    # LOG_LEVEL: str = decouple.config("LOG_LEVEL", cast=str, default="INFO")
    # LOGGERS : tuple = ("uvicorn.asgi", "uvicorn.access", "uvicorn.error", "uvicorn.lifecycle", "uvicorn", "fastapi", "gunicorn", "uvicorn.error", "uvicorn.access", "uvicorn.asgi")
    # LOG_FILE: str = decouple.config("LOG_FILE", cast=str, default=f"{str(ROOT_DIR)}/logs/backend.log")

    # OpenAI settings
    AI_API_KEY: str = decouple.config("AI_API_KEY", cast=str)
    
    # Telegram bot token
    TELEGRAM_BOT_TOKEN: str = decouple.config("TELEGRAM_BOT_TOKEN", cast=str)
    
    # Database settings
    MONGO_HOST: str = decouple.config("MONGO_HOST", cast=str, default="localhost")
    MONGO_PORT: int = decouple.config("MONGO_PORT", cast=int, default=27017)
    MONGO_USERNAME: str = decouple.config("MONGO_USERNAME", cast=str)
    MONGO_PASSWORD: str = decouple.config("MONGO_PASSWORD", cast=str)
    MONGO_DB: str = decouple.config("MONGO_DB", cast=str, default="backend")

    class Config(ConfigDict):
        env_file = f'{str(ROOT_DIR)}/.env'
        case_sensitive = True
        validate_assignment: bool = True
        extra = 'allow'
        
settings = BackendConfig()