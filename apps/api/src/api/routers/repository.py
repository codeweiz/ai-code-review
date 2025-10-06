from typing import Any

from api.ioc.container import ApiContainer
from api.orm.entity.repository import Repository
from common.config import logger
from common.orm.base_repository import BaseRepository
from common.rest.response import BaseResponse
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
@inject
def list_repository(
    repo: BaseRepository[Repository] = Depends(
        Provide[ApiContainer.repository_repository]
    ),
) -> BaseResponse[Any]:
    result = repo.get_all(limit=10)
    logger.info(f"id: {id(repo)}")
    return BaseResponse.success_response(
        data=[r.to_dict() for r in result], message="ok"
    )
