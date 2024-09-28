import boto3
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any
import json

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

    class Config:
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (
                cls.aws_parameter_store_settings,
                cls.aws_secrets_manager_settings,
                env_settings,
                file_secret_settings
            )

        @classmethod
        def aws_parameter_store_settings(cls, settings: BaseSettings) -> dict[str, Any]:
            """Fetch non-sensitive settings from AWS Systems Manager Parameter Store."""
            ssm = boto3.client("ssm")
            parameters = {
                "DATABASE_URL": "/contextual-faq-system/database_url",
            }

            values = {}
            for key, param_name in parameters.items():
                try:
                    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
                    values[key] = response['Parameter']['Value']
                except Exception as e:
                    print(f"Failed to load {key} from Parameter Store: {e}")

            return values

        @classmethod
        def aws_secrets_manager_settings(cls, settings: BaseSettings) -> dict[str, Any]:
            """Fetch sensitive settings from AWS Secrets Manager."""
            secrets_manager = boto3.client("secretsmanager")
            secrets = {
                "OPENAI_API_KEY": "contextual-faq-system/openai",  # Adjusted to your secret names
                "JWT_SECRET_KEY": "contextual-faq-system/jwt"
            }

            values = {}
            for key, secret_name in secrets.items():
                try:
                    response = secrets_manager.get_secret_value(SecretId=secret_name)
                    secret_value = response['SecretString']
                    # If the secret is stored as JSON, parse it
                    if secret_value.startswith('{'):
                        secret_value = json.loads(secret_value)
                        values.update(secret_value)
                    else:
                        values[key] = secret_value
                except Exception as e:
                    print(f"Failed to load {key} from Secrets Manager: {e}")

            return values


# Initialize settings
settings = Settings()
