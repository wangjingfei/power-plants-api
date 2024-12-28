import uvicorn
from app.core.config import settings
from app.main import app
from app.core.database import engine
from app.models import Base

def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)

def main():
    """主函数"""
    # 初始化数据库
    init_db()
    
    # 启动服务
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )

if __name__ == "__main__":
    main() 