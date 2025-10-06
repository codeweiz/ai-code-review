import base64
from typing import Any, Dict, List

import requests
from api.constant.platform import PLATFORM_GITEA
from api.platform.base import GitPlatform, GitPlatformRequest
from api.platform.factory import register_platform
from api.platform.gitea.models import PullRequest, PullRequestFile, CommitItem, FileContent, Webhook
from common.config import appConfig


@register_platform(PLATFORM_GITEA)
class GiteeGitPlatform(GitPlatform):
    """Gitea 实现的代码仓库平台"""

    def __init__(self):
        self.base_url = appConfig.gitea.base_url
        self.token = appConfig.gitea.token

    def request(self, request: GitPlatformRequest) -> Dict[str, Any]:
        url = f"{self.base_url}{request.endpoint}"
        headers = {"Authorization": f"token {self.token}", "Accept": "application/json"}

        resp = requests.request(
            method=request.method,
            url=url,
            params=request.params,
            json=request.data,
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()

    def get_pr_info(self, repo_name: str, pr_number: int) -> PullRequest:
        """获取 Pull Request 基本信息"""

        response = self.request(self._get_pr_info_request(repo_name, pr_number))
        return PullRequest.model_validate(response)

    def get_pr_files(self, repo_name: str, pr_number: int) -> List[PullRequestFile]:
        """获取 Pull Request 相关文件"""

        response = self.request(self._get_pr_files_request(repo_name, pr_number))
        return [PullRequestFile.model_validate(item) for item in response]

    def get_pr_commits(self, repo_name: str, pr_number: int) -> List[CommitItem]:
        """获取 Pull Request 相关提交记录"""

        response = self.request(self._get_pr_commits_request(repo_name, pr_number))
        return [CommitItem.model_validate(item) for item in response]

    def get_file_content(self, repo_name: str, file_path: str, ref: str) -> FileContent:
        """获取文件内容"""

        response = self.request(
            self._get_file_content_request(repo_name, file_path, ref)
        )
        file_content = FileContent.model_validate(response)

        # base64 解码
        if file_content.content:
            file_content.content = base64.b64decode(file_content.content).decode(
                "utf-8"
            )

        return file_content

    def get_webhooks(self, repo_name: str) -> List[Webhook]:
        """获取 webhook 列表"""

        response = self.request(self._get_webhooks_request(repo_name))
        return [Webhook.model_validate(item) for item in response]
