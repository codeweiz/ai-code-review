from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="消息")
    data: Optional[T] = Field(default=None, description="数据")
    success: bool = Field(default=True, description="是否成功")

    @classmethod
    def success_response(
        cls, data: Optional[T] = None, message: str = "操作成功"
    ) -> "BaseResponse[T]":
        return cls(code=200, message=message, data=data, success=True)

    @classmethod
    def error_response(
        cls, code: int = 400, message: str = "操作失败"
    ) -> "BaseResponse[T]":
        return cls(code=code, message=message, data=None, success=False)


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T] = Field(description="数据列表")
    total: int = Field(description="总数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页大小")
    total_pages: int = Field(description="总页数")

    def __init__(self, items: List[T], total: int, page: int, page_size: int, **data):
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        super().__init__(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            **data
        )
