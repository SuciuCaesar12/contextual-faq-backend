from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    LOG_LEVEL: str = 'INFO'
    ECHO_SQL: bool = False
    SIMILARITY_THRESHOLD: float = 0.2
    OPENAI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
