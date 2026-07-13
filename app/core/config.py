from pydantic_settings import BaseSettings,SettingsConfigDict

class Setting(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DATABASE_URL : str
    ALEMBIC_DATABASE_URL: str

    SECRET_KEY : str
    DEBUG: bool = False
    APP_NAME: str = "DecisionAI"

setting = Setting()