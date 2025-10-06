import unittest

from api.constant.platform import PLATFORM_GITEE
from api.constant.rest import REST_METHOD_GET
from api.platform.base import GitPlatformRequest
from api.platform.factory import get_git_platform
from common.config import logger


class TestPlatformGitee(unittest.TestCase):
    """测试 Gitee 平台接口"""

    def setUp(self):
        self.test_owner = "sh_chances"
        self.test_repo = "pulse-guard"
        self.test_pr_number = 3
        self.test_file_name = "Makefile"
        self.test_ref = "ea1bedc646ef55fcb29fb92719aebd7ac522d929"

    def test_request(self):
        """测试访问 Gitee 的仓库信息"""
        gitee_platform = get_git_platform(platform_name=PLATFORM_GITEE)
        request = GitPlatformRequest(
            method=REST_METHOD_GET,
            endpoint=f"/repos/{self.test_owner}/{self.test_repo}",
        )
        resp = gitee_platform.request(request)
        logger.info(resp)

    def test_get_pr_info(self):
        """测试获取 Git Pull Request 信息"""
        gitee_platform = get_git_platform(platform_name=PLATFORM_GITEE)
        resp = gitee_platform.get_pr_info(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            pr_number=self.test_pr_number,
        )
        logger.info(resp)

    def test_get_pr_files(self):
        """测试获取 Git Pull Request files 信息"""
        gitee_platform = get_git_platform(platform_name=PLATFORM_GITEE)
        resp = gitee_platform.get_pr_files(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            pr_number=self.test_pr_number,
        )
        logger.info(resp)

    def test_get_pr_commits(self):
        """测试获取 Git Pull Request commits 信息"""
        gitee_platform = get_git_platform(platform_name=PLATFORM_GITEE)
        resp = gitee_platform.get_pr_commits(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            pr_number=self.test_pr_number,
        )
        logger.info(resp)

    def test_get_file_content(self):
        """测试获取文件内容"""
        gitee_platform = get_git_platform(platform_name=PLATFORM_GITEE)
        resp = gitee_platform.get_file_content(
            repo_name=f"{self.test_owner}/{self.test_repo}",
            file_path=self.test_file_name,
            ref=self.test_ref,
        )
        logger.info(resp)

    def test_get_webhooks(self):
        """测试获取 webhook 列表"""
        gitee_platform = get_git_platform(platform_name=PLATFORM_GITEE)
        resp = gitee_platform.get_webhooks(repo_name="sh_chances/pulse-guard")
        logger.info(resp)
