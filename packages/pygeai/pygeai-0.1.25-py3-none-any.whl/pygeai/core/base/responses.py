from pydantic.main import BaseModel

from pygeai.core.base.models import Error


class ErrorListResponse(BaseModel):
    errors: list[Error]


class EmptyResponse(BaseModel):
    content: dict
