from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int = 27017
    db_auth_source: str = 'admin'

    class Config:
        env_file = './app/.env'


config = ApplicationSettings()
