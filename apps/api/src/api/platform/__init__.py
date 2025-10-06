from .gitea import rest as gitea_rest
from .gitee import rest as gitee_rest
from .github import rest as github_rest

__all__ = ["gitea_rest", "gitee_rest", "github_rest"]
