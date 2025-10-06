import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity.issue import Issue
from api.orm.entity.pull_request_review import PullRequestReview
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestIssueSearch(unittest.TestCase):
    """测试Issue搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self,
        issue_repository: BaseRepository[Issue] = Provide[
            ApiContainer.issue_repository
        ],
    ):
        self.issue_repository = issue_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        repo_list: List[PullRequestReview] = self.issue_repository.get_all(limit=10)
        logger.info(repo_list)

    def test_count(self):
        """测试计数"""
        count = self.issue_repository.count()
        logger.info(count)
