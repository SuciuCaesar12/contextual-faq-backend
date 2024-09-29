from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    
    OPENAI_API_KEY: str
    SIMILARITY_THRESHOLD: float = 0.2
    
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ECHO_SQL: bool = False
    LOG_LEVEL: str = 'INFO'
        
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()

print(settings.DATABASE_URL)
print(settings.OPENAI_API_KEY)
print(settings.JWT_SECRET_KEY)