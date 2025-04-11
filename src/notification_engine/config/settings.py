from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# Load environment variables first to ensure they're available
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    # Environment settings
    environment: str = Field(..., env="ENVIRONMENT")
    log_level: str = Field(..., env="LOG_LEVEL")
    health_check_port: int = Field(..., env="HEALTH_CHECK_PORT")

    # MongoDB settings
    mongo_url: str = Field(..., env="MONGO_URL")
    mongo_db_name: str = Field(..., env="MONGO_DB_NAME")

    # RabbitMQ settings
    rabbitmq_host: str = Field(..., env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(..., env="RABBITMQ_PORT")
    rabbitmq_username: str = Field(..., env="RABBITMQ_USERNAME")
    rabbitmq_password: str = Field(..., env="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field(..., env="RABBITMQ_VHOST")
    rabbitmq_queue_name: str = Field(..., env="RABBITMQ_QUEUE_NAME")
    rabbitmq_ssl: bool = Field(default=True, env="RABBITMQ_SSL")
    rabbitmq_prefetch_count: int = Field(default=10, env="RABBITMQ_PREFETCH_COUNT")
    rabbitmq_retry_count: int = Field(default=3, env="RABBITMQ_RETRY_COUNT")
    rabbitmq_retry_delay: int = Field(default=5, env="RABBITMQ_RETRY_DELAY")

    # OneSignal settings
    onesignal_app_id: str = Field(..., env="ONESIGNAL_APP_ID")
    onesignal_rest_api_key: str = Field(..., env="ONESIGNAL_REST_API_KEY")
    onesignal_api_url: str = Field(..., env="ONESIGNAL_API_URL")
    onesignal_max_retries: int = Field(default=3, env="ONESIGNAL_MAX_RETRIES")
    onesignal_retry_delay: int = Field(default=1, env="ONESIGNAL_RETRY_DELAY")


settings = Settings()

# Print settings for debugging
print(f"Environment: {settings.environment}")
print(f"MongoDB: {settings.mongo_url}, DB: {settings.mongo_db_name}")
print(f"RabbitMQ: {settings.rabbitmq_host}:{settings.rabbitmq_port}")
print(f"OneSignal: {settings.onesignal_app_id}")
