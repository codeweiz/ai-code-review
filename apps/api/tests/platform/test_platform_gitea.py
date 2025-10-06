import unittest

from api.constant.platform import PLATFORM_GITEA
from api.constant.rest import REST_METHOD_GET
from api.platform.base import GitPlatformRequest
from api.platform.factory import get_git_platform
from common.config import logger


class TestPlatformGitea(unittest.TestCase):
    """测试 Gitea 平台接口"""

    def setUp(self):
        self.test_owner = "gsfs"
        self.test_repo = "portal_common_core"
        self.test_pr_number = 1
        self.test_file_name = "src/directives/permission.ts"
        self.test_ref = "a77513be75ce34014e7d43c21dc4eff87ffa65ac"

    def test_request(self):
        """测试访问 Gitea 的仓库信息"""
        gitea_platform = get_git_platform(platform_name=PLATFORM_GITEA)
        request = GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{self.test_owner}/{self.test_repo}",
        )
        resp = gitea_platform.request(request)
        logger.info(resp)

    def test_get_pr_info(self):
        """测试获取 Git Pull Request 信息"""
        gitea_platform = get_git_platform(platform_name=PLATFORM_GITEA)
        resp = gitea_platform.get_pr_info(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            pr_number=self.test_pr_number,
        )
        logger.info(resp)

    def test_get_pr_files(self):
        """测试获取 Git Pull Request files 信息"""
        gitea_platform = get_git_platform(platform_name=PLATFORM_GITEA)
        resp = gitea_platform.get_pr_files(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            pr_number=self.test_pr_number,
        )
        logger.info(resp)

    def test_get_pr_commits(self):
        """测试获取 Git Pull Request commits 信息"""
        gitea_platform = get_git_platform(platform_name=PLATFORM_GITEA)
        resp = gitea_platform.get_pr_commits(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            pr_number=self.test_pr_number,
        )
        logger.info(resp)

    def test_get_file_content(self):
        """测试获取文件内容"""
        gitea_platform = get_git_platform(platform_name=PLATFORM_GITEA)
        resp = gitea_platform.get_file_content(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            file_path=self.test_file_name,
            ref=self.test_ref,
        )
        logger.info(resp)

    def test_get_webhooks(self):
        """测试获取 webhook 列表"""
        gitea_platform = get_git_platform(platform_name=PLATFORM_GITEA)
        resp = gitea_platform.get_webhooks(
            repo_name=f"{self.test_owner}/{self.test_repo}"
        )
        logger.info(resp)
