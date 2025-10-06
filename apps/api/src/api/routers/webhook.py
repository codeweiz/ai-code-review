from common.config import logger
from common.exception import VectorStoreError
from common.rest.response import BaseResponse
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/github")
async def github(request: Request):
    """GitHub webhook"""
    try:
        logger.info(f"GitHub webhook: {request.__dict__}")
        return BaseResponse.success_response(data=[])
    except Exception as e:
        logger.error(f"接收GitHub webhook失败: {e}")
        raise VectorStoreError(message="接收GitHub webhook失败", detail=str(e))


@router.post("/gitee")
async def gitee(request: Request):
    """Gitee webhook"""
    try:
        logger.info(f"Gitee webhook: {request.__dict__}")
        return BaseResponse.success_response(data=[])
    except Exception as e:
        logger.error(f"接收Gitee webhook失败: {e}")
        raise VectorStoreError(message="接收Gitee webhook失败", detail=str(e))


@router.post("/gitea")
async def gitea(request: Request):
    """Gitea webhook"""
    try:
        logger.info(f"Gitea webhook: {request.__dict__}")
        return BaseResponse.success_response(data=[])
    except Exception as e:
        logger.error(f"接收Gitea webhook失败: {e}")
        raise VectorStoreError(message="接收Gitea webhook失败", detail=str(e))
