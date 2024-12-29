import os
import uvicorn
from app.core.config import settings
from app.main import app
from app.core.database import engine
from app.models import Base

def init_dirs():
    """初始化必要的目录"""
    # 创建日志目录
    log_dir = os.path.dirname(settings.LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建配置目录
    config_dir = os.path.dirname(settings.CONFIG_FILE)
    os.makedirs(config_dir, exist_ok=True)

def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)

def main():
    """主函数"""
    # 初始化目录
    init_dirs()
    
    # 初始化数据库
    init_db()
    
    # 启动服务
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS
    )

if __name__ == "__main__":
    main() 