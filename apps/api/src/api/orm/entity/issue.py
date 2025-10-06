from datetime import datetime

from common.orm.base import Base
from sqlalchemy import DATETIME, Column, Integer, String, Text


class Issue(Base):
    """Issue表"""

    __tablename__ = "cs_pr_issue"

    # id
    id = Column(Integer, name="id", primary_key=True, index=True)
    created_at = Column(DATETIME, name="created_at", default=datetime.now)
    created_by = Column(DATETIME, name="created_by", nullable=True)
    updated_at = Column(DATETIME, name="updated_at", default=datetime.now)
    updated_by = Column(DATETIME, name="updated_by", nullable=True)

    # PR 评审 ID
    pull_request_review_id = Column(
        Integer, name="pull_request_review_id", nullable=False
    )
    # semgrep、llm、eslint、sonarqube
    source = Column(String(50), name="source", nullable=False)
    # 静态工具的规则ID
    rule_id = Column(String(255), name="rule_id", nullable=True)
    # 问题分类：security、design、quality、practice、performance、bug
    type = Column(String(50), name="type", nullable=True)
    # 严重程度：critical、high、medium、low
    severity = Column(String(20), name="severity", nullable=True)
    # 分类：sql_injection、null_pointer
    category = Column(String(100), name="category", nullable=True)

    # 问题描述
    # 标题
    title = Column(Text, name="title", nullable=False)
    # 描述
    description = Column(Text, name="description", nullable=True)
    # 影响
    impact = Column(Text, name="impact", nullable=True)
    # 修复建议
    suggestion = Column(Text, name="suggestion", nullable=True)

    # 状态：active、fixed、exempted、ignored
    status = Column(String(50), name="status", default="active", nullable=False)

    def __repr__(self):
        return (
            f"<PullRequest(id={self.id}, created_at='{self.created_at}, created_by='{self.created_by}, updated_at='{self.updated_at}, updated_by='{self.updated_by}, "
            f"pull_request_review_id='{self.pull_request_review_id}, source='{self.source}, rule_id='{self.rule_id}, type='{self.type}, severity='{self.severity}, category='{self.category}"
            f", title='{self.title}, description='{self.description}, impact='{self.impact}, "
            f"suggestion='{self.suggestion}, status='{self.status}>"
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by,
            "pull_request_review_id": self.pull_request_review_id,
            "source": self.source,
            "rule_id": self.rule_id,
            "type": self.type,
            "severity": self.severity,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "suggestion": self.suggestion,
            "status": self.status,
        }
