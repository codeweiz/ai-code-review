from common.orm.base import Base
from sqlalchemy import Column, String


class Type(Base):
    """内容基础类型"""

    __tablename__ = "EPG_TYPE"

    # 编码
    code = Column(String(50), name="CODE", primary_key=True, nullable=True)

    # 名称
    name = Column(String(500), name="NAME", nullable=False)

    def __repr__(self):
        return f"<Type(name={self.name}, code='{self.code}')>"

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "code": self.code,
        }
