from pydantic_settings import BaseSettings
from typing import Optional
import configparser
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI CRUD API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 配置文件路径
    CONFIG_FILE: str = "/etc/power-plant/config.ini"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_config()
    
    def load_config(self):
        """从配置文件加载配置"""
        if not os.path.exists(self.CONFIG_FILE):
            raise FileNotFoundError(f"配置文件不存在: {self.CONFIG_FILE}")
            
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)
        
        # 数据库配置
        db_config = config['database']
        self.DATABASE_URL = (
            f"mysql+pymysql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config.get('port', '3306')}/{db_config['database']}"
            f"?charset=utf8mb4"
        )
        self.DB_DEBUG = db_config.getboolean('debug', fallback=False)
        
        # 应用配置
        if 'app' in config:
            app_config = config['app']
            self.DEBUG = app_config.getboolean('DEBUG', fallback=False)
            self.WORKERS = app_config.getint('WORKERS', fallback=1)
            self.HOST = app_config.get('HOST', fallback='0.0.0.0')
            self.PORT = app_config.getint('PORT', fallback=8000)
        
        # 日志配置
        if 'logging' in config:
            log_config = config['logging']
            self.LOG_LEVEL = log_config.get('LEVEL', fallback='INFO')
            self.LOG_FILE = log_config.get('FILE', fallback='/var/log/power-plant/app.log')

    class Config:
        env_file = ".env"

settings = Settings()