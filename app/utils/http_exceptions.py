from typing import Any, Dict
from fastapi import HTTPException
from http import HTTPStatus


class ResourceNotFoundException(HTTPException):

    DEFAULT_MESSAGE = "Recurso não existe ou foi deletado"

    def __init__(self, status_code: int = HTTPStatus.NOT_FOUND, detail: str = DEFAULT_MESSAGE, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code, detail, headers)


class NoContentException(HTTPException):

    DEFAULT_MESSAGE = "Recurso solicitado não contém registros"

    def __init__(self, status_code: int = HTTPStatus.NO_CONTENT, detail: str = DEFAULT_MESSAGE, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code, detail, headers)        


class ResourceConflictException(HTTPException):
        
    DEFAULT_MESSAGE = "Recurso solicitado não contém registros"

    def __init__(self, status_code: int = HTTPStatus.CONFLICT, detail: str = DEFAULT_MESSAGE, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code, detail, headers)  


class ResourceExpectationFailedException:
        
    DEFAULT_MESSAGE = "Operação Inválida"

    def __init__(self, status_code: int = HTTPStatus.EXPECTATION_FAILED, detail: str = DEFAULT_MESSAGE, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code, detail, headers)  