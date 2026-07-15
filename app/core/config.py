from pydantic_settings import BaseSettings,SettingsConfigDict

class Setting(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DATABASE_URL : str
    ALEMBIC_DATABASE_URL: str

    SECRET_KEY : str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False
    APP_NAME: str = "DecisionAI"

setting = Setting()