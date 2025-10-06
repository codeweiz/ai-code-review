from contextlib import asynccontextmanager
from typing import AsyncGenerator

from common.config import logger
from common.exception import APIException
from common.rest.response import BaseResponse
from dependency_injector import providers
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .ioc.container import ApiContainer
from .routers import webhook
from .routers.database import (issue, pull_request, pull_request_review,
                               repository)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up API server")
    yield
    logger.info("Shutting down API server")


# 初始化 DI 容器
container = ApiContainer()
container.wire(modules=[repository, pull_request, pull_request_review, issue, webhook])


# 预热 IOC 单例
def preload_singletons(container):
    for provider in container.traverse():
        if isinstance(provider, providers.Singleton):
            try:
                provider()
            except Exception as e:
                target = getattr(provider.provides, "__name__", str(provider.provides))
                print(f"单例 {target} 预热失败: {e}")


preload_singletons(container)

app = FastAPI(
    title="Content Vector Engine API",
    description="内容向量引擎API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repository.router, prefix="/api/v1/db/repository", tags=["仓库 SQL"])
app.include_router(
    pull_request.router, prefix="/api/v1/db/pull_request", tags=["Pull Request SQL"]
)
app.include_router(
    pull_request_review.router,
    prefix="/api/v1/db/pull_request_review",
    tags=["Pull Request Review SQL"],
)
app.include_router(
    issue.router,
    prefix="/api/v1/db/issue",
    tags=["Pull Request Review SQL"],
)
app.include_router(webhook.router, prefix="/api/v1/webhook", tags=["WebHook"])


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content=BaseResponse.error_response(
            code=exc.code, message=exc.message
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=BaseResponse.error_response(
            code=422, message="请求参数验证失败"
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponse.error_response(
            code=500, message="服务器内部错误"
        ).model_dump(),
    )


@app.get("/", response_model=BaseResponse[str])
async def root():
    return BaseResponse.success_response(
        data="Content Vector Engine API", message="API服务正常运行"
    )


@app.get("/health", response_model=BaseResponse[str])
async def health_check():
    return BaseResponse.success_response(data="healthy", message="服务健康")
