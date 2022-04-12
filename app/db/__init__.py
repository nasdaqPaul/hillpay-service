from mongoengine import connect
from app.config import config


connect(host=f'mongodb://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}?authSource={config.db_auth_source}')
