from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

# Debug code removed to avoid printing sensitive environment variables


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    host: str = Field(default="localhost", env="RABBITMQ_HOST")
    port: int = Field(default=5672, env="RABBITMQ_PORT")
    username: str = Field(default="guest", env="RABBITMQ_USERNAME")
    password: str = Field(default="guest", env="RABBITMQ_PASSWORD")
    vhost: str = Field(default="/", env="RABBITMQ_VHOST")
    queue_name: str = Field(default="notification", env="RABBITMQ_NAME")
    prefetch_count: int = Field(default=10, env="RABBITMQ_PREFETCH_COUNT")
    retry_count: int = Field(default=3, env="RABBITMQ_RETRY_COUNT")
    retry_delay: int = Field(default=5, env="RABBITMQ_RETRY_DELAY")


class OneSignalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    app_id: str = Field(
        default="376dc542-b47f-42fb-bf6e-88c371ae68de", env="ONESIGNAL_APP_ID"
    )
    rest_api_key: str = Field(
        default="os_v2_app_g5w4kqvup5bpxp3ordbxdlti3zv7ugyznrbudmma3rwhmb5pge4gcznyiuigoseroiqgflrlv7lbapjbrrxbd5cspxgtdgtmfhw5oza",
        env="ONESIGNAL_REST_API_KEY",
    )
    api_url: str = Field(
        default="https://onesignal.com/api/v1", env="ONESIGNAL_API_URL"
    )
    max_retries: int = Field(default=3, env="ONESIGNAL_MAX_RETRIES")
    retry_delay: int = Field(default=1, env="ONESIGNAL_RETRY_DELAY")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    onesignal: OneSignalSettings = OneSignalSettings()
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    health_check_port: int = Field(default=8000, env="HEALTH_CHECK_PORT")
    mongo_url: str = Field(
        default="mongodb+srv://devUser:flowbeedev@development.nenpl.mongodb.net/?retryWrites=true&w=majority&appName=Developmen",
        env="MONGO_URL",
    )
    mongo_db_name: str = Field(default="Notification", env="MONGO_DB_NAME")


settings = Settings()
print(settings.model_dump_json())
