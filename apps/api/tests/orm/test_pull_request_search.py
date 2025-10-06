import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity.pull_request import PullRequest
from api.orm.entity.repository import Repository
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestPullRequestSearch(unittest.TestCase):
    """测试PullRequest搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self,
        pull_request_repository: BaseRepository[Repository] = Provide[
            ApiContainer.pull_request_repository
        ],
    ):
        self.pull_request_repository = pull_request_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        repo_list: List[PullRequest] = self.pull_request_repository.get_all(limit=10)
        logger.info(repo_list)

    def test_count(self):
        """测试计数"""
        count = self.pull_request_repository.count()
        logger.info(count)
