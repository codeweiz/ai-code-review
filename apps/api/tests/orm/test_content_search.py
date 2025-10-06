import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity import Content
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestContentSearch(unittest.TestCase):
    """测试内容搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self,
        content_repository: BaseRepository[Content] = Provide[
            ApiContainer.content_repository
        ],
    ):
        self.content_repository = content_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        content_list: List[Content] = self.content_repository.get_all(limit=10)
        logger.info(content_list)

    def test_count(self):
        """测试计数"""
        count = self.content_repository.count()
        logger.info(count)

    def test_get_by_filters(self):
        """根据过滤器获取记录"""
        content_codes = [
            "02000002000000012018050999164116",
            "02000003000000012023081699001089",
        ]
        contents: List[Content] = self.content_repository.get_by_filters(
            {"content_code__in": content_codes}
        )
        logger.info(contents)
