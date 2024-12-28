from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any

@as_declarative()
class Base:
    """
    SQLAlchemy 模型的基类
    """
    id: Any
    __name__: str

    # 生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        """
        将类名转换为小写作为表名
        """
        return cls.__name__.lower() 