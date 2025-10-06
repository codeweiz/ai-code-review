class APIException(Exception):
    def __init__(self, code: int = 400, message: str = "API Error", detail: str = None):
        self.code = code
        self.message = message
        self.detail = detail
        super().__init__(message)


class ValidationException(APIException):
    def __init__(self, message: str = "Validation Error", detail: str = None):
        super().__init__(code=400, message=message, detail=detail)


class NotFoundError(APIException):
    def __init__(self, message: str = "Resource Not Found", detail: str = None):
        super().__init__(code=404, message=message, detail=detail)


class InternalServerError(APIException):
    def __init__(self, message: str = "Internal Server Error", detail: str = None):
        super().__init__(code=500, message=message, detail=detail)


class DatabaseError(APIException):
    def __init__(self, message: str = "Database Error", detail: str = None):
        super().__init__(code=500, message=message, detail=detail)


class VectorStoreError(APIException):
    def __init__(self, message: str = "Vector Store Error", detail: str = None):
        super().__init__(code=500, message=message, detail=detail)


class ElasticsearchError(APIException):
    def __init__(self, message: str = "Elasticsearch Error", detail: str = None):
        super().__init__(code=500, message=message, detail=detail)
