import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity.repository import Repository
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestRepositorySearch(unittest.TestCase):
    """测试仓库搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
            self,
            repository_repository: BaseRepository[Repository] = Provide[
                ApiContainer.repository_repository
            ],
    ):
        self.repository_repository = repository_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        repo_list: List[Repository] = self.repository_repository.get_all(limit=10)
        logger.info(repo_list)

    def test_count(self):
        """测试计数"""
        count = self.repository_repository.count()
        logger.info(count)
