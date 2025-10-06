from common.orm.base import Base
from sqlalchemy import Column, String


class Frame(Base):
    """截帧实体"""

    __tablename__ = "cms_frame"

    # 内容编码，唯一键
    content_code = Column(String(50), primary_key=True, nullable=False)
    # 时间：格式 hhmmss
    time = Column(String(50), nullable=False)
    # 图片地址
    url = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<Frame(content_code={self.content_code}, time='{self.time}', url='{self.url}'>"

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "content_code": self.content_code,
            "time": self.time,
            "url": self.url,
        }
