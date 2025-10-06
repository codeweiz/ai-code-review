from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from api.constant.rest import REST_METHOD_GET
from pydantic import BaseModel, Field


class GitPlatformRequest(BaseModel):
    """Git 平台请求"""

    method: str = Field(..., description="请求方法")

    endpoint: str = Field(..., description="请求端点")

    params: Optional[Dict[str, Any]] = Field(default=None, description="请求参数")

    data: Optional[Dict[str, Any]] = Field(default=None, description="请求体")

    headers: Optional[Dict[str, str]] = Field(default=None, description="请求头")


class GitPlatform(ABC):
    """代码仓库平台"""

    @abstractmethod
    def request(self, request: GitPlatformRequest) -> Dict[str, Any]:
        pass

    def _get_pr_info_request(
        self, repo_name: str, pr_number: int
    ) -> GitPlatformRequest:
        """获取 Pull Request 基本信息的请求"""

        return GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{repo_name}/pulls/{pr_number}",
        )

    @abstractmethod
    def get_pr_info(self, repo_name: str, pr_number: int) -> BaseModel:
        """获取 Pull Request 基本信息"""
        pass

    def _get_pr_files_request(
        self, repo_name: str, pr_number: int
    ) -> GitPlatformRequest:
        """获取 Pull Request 相关文件的请求"""

        return GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{repo_name}/pulls/{pr_number}/files",
        )

    @abstractmethod
    def get_pr_files(self, repo_name: str, pr_number: int) -> List[BaseModel]:
        """获取 Pull Request 相关文件"""
        pass

    def _get_pr_commits_request(
        self, repo_name: str, pr_number: int
    ) -> GitPlatformRequest:
        """获取 Pull Request 相关提交记录的请求"""

        return GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{repo_name}/pulls/{pr_number}/commits",
        )

    @abstractmethod
    def get_pr_commits(self, repo_name: str, pr_number: int) -> List[BaseModel]:
        """获取 Pull Request 相关提交记录"""
        pass

    def _get_file_content_request(
        self, repo_name: str, file_path: str, ref: str
    ) -> GitPlatformRequest:
        """获取文件内容的请求"""

        return GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{repo_name}/contents/{file_path}",
            params={"ref": ref},
        )

    @abstractmethod
    def get_file_content(self, repo_name: str, file_path: str, ref: str) -> BaseModel:
        """获取文件内容"""
        pass

    def _get_webhooks_request(self, repo_name: str) -> GitPlatformRequest:
        """获取 webhook 列表的请求"""

        return GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{repo_name}/hooks",
        )

    @abstractmethod
    def get_webhooks(self, repo_name: str) -> List[BaseModel]:
        """获取 webhook 列表"""
        pass
