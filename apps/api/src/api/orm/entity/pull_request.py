from datetime import datetime

from common.orm.base import Base
from sqlalchemy import DATETIME, Boolean, Column, Integer, String, Text


class PullRequest(Base):
    """PR表"""

    __tablename__ = "cs_pr_pull_request"

    # id
    id = Column(Integer, name="id", primary_key=True, index=True)
    created_at = Column(DATETIME, name="created_at", default=datetime.now)
    created_by = Column(DATETIME, name="created_by", nullable=True)
    updated_at = Column(DATETIME, name="updated_at", default=datetime.now)
    updated_by = Column(DATETIME, name="updated_by", nullable=True)

    # Git 信息
    # 仓库 ID
    repository_id = Column(String(255), name="repository_id", nullable=False)
    # PR ID
    pr_id = Column(String(255), name="pr_id", nullable=False)
    # PR number
    pr_number = Column(Integer, name="pr_number", nullable=False)

    # PR 基本信息
    # 标题
    title = Column(Text, name="title", nullable=False)
    # 描述
    description = Column(Text, name="description", nullable=True)
    # 源分支
    source_branch = Column(String(255), name="source_branch", nullable=False)
    # 目标分支
    target_branch = Column(String(255), name="target_branch", nullable=False)
    # 作者
    author = Column(String(255), name="author", nullable=False)
    # 作者邮箱
    author_email = Column(String(255), name="author_email", nullable=True)

    # PR 状态
    # 状态：open、merged、closed、draft
    status = Column(String(50), name="status", default="open", nullable=False)
    # 是否为草稿
    is_draft = Column(Boolean, name="is_draft", default=False, nullable=False)

    # 代码统计
    # 文件改动数量
    files_changed = Column(Integer, name="files_changed", default=0, nullable=False)
    # 新增行数
    lines_added = Column(Integer, name="lines_added", default=0, nullable=False)
    # 删除行数
    lines_deleted = Column(Integer, name="lines_deleted", default=0, nullable=False)
    # 提交数量
    commits_count = Column(Integer, name="commits_count", default=0, nullable=False)

    # 审查相关
    # 审查状态：pending、in_progress、completed、failed
    review_status = Column(
        String(50), name="review_status", default="pending", nullable=False
    )
    # 上次审查时间
    last_review_at = Column(DATETIME, name="last_review_at", nullable=True)
    # 审查触发：webhook、manual、scheduled
    review_triggered_by = Column(String(50), name="review_triggered_by", nullable=True)

    def __repr__(self):
        return (
            f"<PullRequest(id={self.id}, created_at='{self.created_at}, created_by='{self.created_by}, updated_at='{self.updated_at}, updated_by='{self.updated_by}, "
            f"repository_id='{self.repository_id}, pr_id='{self.pr_id}, pr_number='{self.pr_number}, title='{self.title}, description='{self.description}, source_branch='{self.source_branch}"
            f", target_branch='{self.target_branch}, author='{self.author}, author_email='{self.author_email}, "
            f"status='{self.status}, is_draft='{self.is_draft}, files_changed='{self.files_changed}, lines_added='{self.lines_added}, "
            f"lines_deleted='{self.lines_deleted}'), commits_count='{self.commits_count}, review_status='{self.review_status}, last_review_at='{self.last_review_at}, review_triggered_by='{self.review_triggered_by}>"
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by,
            "repository_id": self.repository_id,
            "pr_id": self.pr_id,
            "pr_number": self.pr_number,
            "title": self.title,
            "description": self.description,
            "source_branch": self.source_branch,
            "target_branch": self.target_branch,
            "author": self.author,
            "author_email": self.author_email,
            "status": self.status,
            "is_draft": self.is_draft,
            "files_changed": self.files_changed,
            "lines_added": self.lines_added,
            "lines_deleted": self.lines_deleted,
            "commits_count": self.commits_count,
            "review_status": self.review_status,
            "last_review_at": self.last_review_at,
            "review_triggered_by": self.review_triggered_by,
        }
