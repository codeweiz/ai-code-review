import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity.type import Type
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestTypeSearch(unittest.TestCase):
    """测试内容类型搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self,
        type_repository: BaseRepository[Type] = Provide[ApiContainer.type_repository],
    ):
        self.type_repository = type_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        type_list: List[Type] = self.type_repository.get_all(limit=10)
        logger.info(type_list)

    def test_count(self):
        """测试计数"""
        count = self.type_repository.count()
        logger.info(count)

    def test_get_by_filters(self):
        """根据过滤器获取记录"""
        type_codes = [
            "001",
            "002",
        ]
        type_list: List[Type] = self.type_repository.get_by_filters(
            {"code__in": type_codes}
        )
        logger.info(type_list)
