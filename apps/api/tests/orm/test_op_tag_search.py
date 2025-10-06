import unittest
from typing import List

from api.ioc.container import ApiContainer
from api.orm.entity.op_tag import OpTag
from common.config import logger
from common.orm.base_repository import BaseRepository
from dependency_injector.wiring import Provide, inject


class TestOpTagSearch(unittest.TestCase):
    """测试运营标签搜索"""

    @classmethod
    def setUpClass(cls):
        cls.container = ApiContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self,
        op_tag_repository: BaseRepository[OpTag] = Provide[
            ApiContainer.op_tag_repository
        ],
    ):
        self.op_tag_repository = op_tag_repository

    def test_search_limit_10(self):
        """测试搜索结果数量限制"""
        op_tag_list: List[OpTag] = self.op_tag_repository.get_all(limit=10)
        logger.info(op_tag_list)

    def test_count(self):
        """测试计数"""
        count = self.op_tag_repository.count()
        logger.info(count)

    def test_get_by_filters(self):
        """根据过滤器获取记录"""
        op_tag_codes = [
            "0051",
            "0053",
        ]
        op_tag_list: List[OpTag] = self.op_tag_repository.get_by_filters(
            {"code__in": op_tag_codes}
        )
        logger.info(op_tag_list)
