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


print('OPENAI_API_KEY')
print(f'Type: {type(settings.OPENAI_API_KEY)}')
print(f'Value: {settings.OPENAI_API_KEY}')

print('JWT_SECRET_KEY')
print(f'Type: {type(settings.JWT_SECRET_KEY)}')
print(f'Value: {settings.JWT_SECRET_KEY}')

# if isinstance(settings.OPENAI_API_KEY, dict):
#     print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY}")
#     settings.OPENAI_API_KEY = settings.OPENAI_API_KEY['OPENAI_API_KEY']

# if isinstance(settings.JWT_SECRET_KEY, dict):
#     print(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")
#     settings.JWT_SECRET_KEY = settings.JWT_SECRET_KEY['JWT_SECRET_KEY']
    
# print(settings.DATABASE_URL)
# print(settings.OPENAI_API_KEY)
# print(settings.JWT_SECRET_KEY)

    