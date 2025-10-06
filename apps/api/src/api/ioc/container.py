from api.orm.entity.issue import Issue
from api.orm.entity.pull_request import PullRequest
from api.orm.entity.pull_request_review import PullRequestReview
from api.orm.entity.repository import Repository
from common.ioc.container import CommonContainer
from common.orm.base_repository import BaseRepository
from dependency_injector import containers, providers


class ApiContainer(containers.DeclarativeContainer):
    """API 容器，管理应用层的依赖"""

    common = providers.Container(CommonContainer)

    repository_repository = providers.Factory(
        BaseRepository,
        model=Repository,
        db_factory=common.container.db_session_factory,
        datasource="master",
    )

    pull_request_repository = providers.Factory(
        BaseRepository,
        model=PullRequest,
        db_factory=common.container.db_session_factory,
        datasource="master",
    )

    pull_request_review_repository = providers.Factory(
        BaseRepository,
        model=PullRequestReview,
        db_factory=common.container.db_session_factory,
        datasource="master",
    )

    issue_repository = providers.Factory(
        BaseRepository,
        model=Issue,
        db_factory=common.container.db_session_factory,
        datasource="master",
    )
