from datetime import datetime

from common.orm.base import Base
from sqlalchemy import DATETIME, Column, Integer, String, Text


class PrReview(Base):
    """Pull Request Review 表，一个 PR 可能被评审多次"""

    __tablename__ = "cs_pr_pull_request_review"

    # id
    id = Column(Integer, name="id", primary_key=True, index=True)
    created_at = Column(DATETIME, name="created_at", default=datetime.now)
    created_by = Column(DATETIME, name="created_by", nullable=True)
    updated_at = Column(DATETIME, name="updated_at", default=datetime.now)
    updated_by = Column(DATETIME, name="updated_by", nullable=True)

    pull_request_id = Column(Integer, name="pull_request_id", nullable=False)
    review_number = Column(Integer, name="review_number", default=0, nullable=False)
    git_commit_sha = Column(String(64), name="git_commit_sha", nullable=False)

    # 评分
    # 总分
    total_score = Column(Integer, name="total_score", default=0, nullable=True)
    # 安全评分
    secure_score = Column(Integer, name="secure_score", default=0, nullable=True)
    # 架构评分
    design_score = Column(Integer, name="design_score", default=0, nullable=True)
    # 质量评分
    quality_score = Column(Integer, name="quality_score", default=0, nullable=True)
    # 练习评分
    practice_score = Column(Integer, name="practice_score", default=0, nullable=True)
    # 性能评分
    performance_score = Column(
        Integer, name="performance_score", default=0, nullable=True
    )

    # 处理状态
    # 状态：running、completed、failed、canceled
    status = Column(String(50), name="status", default="running", nullable=False)
    # 错误信息
    error_message = Column(Text, name="error_message", nullable=True)

    def __repr__(self):
        return (
            f"<PullRequest(id={self.id}, created_at='{self.created_at}, created_by='{self.created_by}, updated_at='{self.updated_at}, updated_by='{self.updated_by}, "
            f"pull_request_id='{self.pull_request_id}, review_number='{self.review_number}, git_commit_sha='{self.git_commit_sha}, total_score='{self.total_score}, secure_score='{self.secure_score}, design_score='{self.design_score}"
            f", quality_score='{self.quality_score}, practice_score='{self.practice_score}, performance_score='{self.performance_score}, "
            f"status='{self.status}, error_message='{self.error_message}>"
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by,
            "pull_request_id": self.pull_request_id,
            "review_number": self.review_number,
            "git_commit_sha": self.git_commit_sha,
            "total_score": self.total_score,
            "secure_score": self.secure_score,
            "design_score": self.design_score,
            "quality_score": self.quality_score,
            "practice_score": self.practice_score,
            "performance_score": self.performance_score,
            "status": self.status,
            "error_message": self.error_message,
        }
