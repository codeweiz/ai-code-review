from api.orm.entity import Content
from api.orm.entity.base_tag import BaseTag
from api.orm.entity.op_tag import OpTag
from api.orm.entity.type import Type
from common.ioc.container import CommonContainer
from common.orm.base_repository import BaseRepository
from dependency_injector import containers, providers


class ApiContainer(containers.DeclarativeContainer):
    """API 容器，管理应用层的依赖"""

    common = providers.Container(CommonContainer)

    content_repository = providers.Factory(
        BaseRepository,
        model=Content,
        db_factory=common.container.db_session_factory,
        datasource="epg_content",
    )

    base_tag_repository = providers.Factory(
        BaseRepository,
        model=BaseTag,
        db_factory=common.container.db_session_factory,
        datasource="epg_content",
    )

    op_tag_repository = providers.Factory(
        BaseRepository,
        model=OpTag,
        db_factory=common.container.db_session_factory,
        datasource="epg_content",
    )

    type_repository = providers.Factory(
        BaseRepository,
        model=Type,
        db_factory=common.container.db_session_factory,
        datasource="epg_content",
    )
