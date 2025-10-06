from typing import Any

from api.ioc.container import ApiContainer
from api.orm.entity import Content
from common.ai.llm.llm_client import LLMClient
from common.config import logger
from common.orm.base_repository import BaseRepository
from common.rest.response import BaseResponse
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
@inject
def list_content(
    repo: BaseRepository[Content] = Depends(Provide[ApiContainer.content_repository]),
) -> BaseResponse[Any]:
    result = repo.get_all(limit=10)
    logger.info(f"id: {id(repo)}")
    return BaseResponse.success_response(
        data=[r.to_dict() for r in result], message="ok"
    )


@router.get("/chat")
@inject
async def chat_content(
    llm: LLMClient = Depends(Provide[ApiContainer.common.llm_client]),
) -> BaseResponse[Any]:
    logger.info(f"id: {id(llm)}")
    response = await llm.client.ainvoke(input="你好")
    return BaseResponse.success_response(data=response.content, message="ok")
