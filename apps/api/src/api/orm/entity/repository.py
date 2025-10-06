from common.orm.base import Base
from sqlalchemy import Boolean, Column, Integer, String


class Repository(Base):
    """仓库表"""

    __tablename__ = "cs_pr_repository"

    # id
    id = Column(Integer, name="id", primary_key=True, index=True)

    # Git 信息
    # 仓库 ID
    repo_id = Column(String(255), name="repo_id", nullable=False)
    # 仓库全名：owner/repo
    full_name = Column(String(255), name="full_name", nullable=False)
    # 名称：XX仓库
    name = Column(String(255), name="name", nullable=False)
    # 默认分支：master
    default_branch = Column(
        String(100), name="default_branch", default="master", nullable=False
    )

    # 管理状态
    # 启用/禁用状态
    enable_status = Column(Boolean, name="enable_status", default=True, nullable=False)
    # 删除状态
    delete_flag = Column(Boolean, name="delete_flag", default=False, nullable=False)

    def __repr__(self):
        return (
            f"<Repository(id={self.id}, repo_id='{self.repo_id}, full_name='{self.full_name}, name='{self.name}"
            f", default_branch='{self.default_branch}, enable_status='{self.enable_status}, delete_flag='{self.delete_flag}')>"
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "repo_id": self.repo_id,
            "full_name": self.full_name,
            "name": self.name,
            "default_branch": self.default_branch,
            "enable_status": self.enable_status,
            "delete_flag": self.delete_flag,
        }
