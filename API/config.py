from pydantic import BaseSettings

class RedisSettings(BaseSettings):
    database_hostname: str
    redis_database_port: str
    db: int

    class Config:
        env_file = ".env"

class PostgresSettings(BaseSettings):
    database_hostname: str
    postgres_database_port: str
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env"



redis_settings =  RedisSettings()
postgres_settings = PostgresSettings()