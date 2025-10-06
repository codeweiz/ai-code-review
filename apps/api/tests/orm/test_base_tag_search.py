import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity.base_tag import BaseTag
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestBaseTagSearch(unittest.TestCase):
    """测试基础标签搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self,
        base_tag_repository: BaseRepository[BaseTag] = Provide[
            ApiContainer.base_tag_repository
        ],
    ):
        self.base_tag_repository = base_tag_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        base_tag_list: List[BaseTag] = self.base_tag_repository.get_all(limit=10)
        logger.info(base_tag_list)

    def test_count(self):
        """测试计数"""
        count = self.base_tag_repository.count()
        logger.info(count)

    def test_get_by_filters(self):
        """根据过滤器获取记录"""
        base_tag_codes = [
            "0001",
            "0005",
        ]
        base_tag_list: List[BaseTag] = self.base_tag_repository.get_by_filters(
            {"code__in": base_tag_codes}
        )
        logger.info(base_tag_list)
