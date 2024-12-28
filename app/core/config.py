from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI CRUD API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"  # 默认配置
    
    @property
    def get_database_url(self) -> str:
        """从配置文件读取数据库连接URL"""
        try:
            import jproperties
            
            with open('/opt/power-plants/config/database.conf', 'rb') as f:
                props = jproperties.Properties()
                props.load(f)
                
                host = props.get('database.host').data
                dbname = props.get('database.name').data
                user = props.get('database.user').data
                password = props.get('database.password').data
                
                return f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
        except (FileNotFoundError, KeyError):
            return self.DATABASE_URL  # 如果配置文件不存在或缺少必要配置则使用默认配置

    class Config:
        env_file = ".env"

settings = Settings() 