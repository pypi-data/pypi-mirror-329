from typing import Union, Optional, Any
from datetime import datetime
from datamodel import BaseModel, Field
from ..datasources.drivers import SUPPORTED

def supported_drivers(field, driver, **kwargs):  # pylint: disable=W0613
    return driver in SUPPORTED


class Query(BaseModel):
    """Represents the entry of a query to be executed.
    """
    driver: str = Field(required=False, default='pg', validator=supported_drivers)
    datasource: str = Field(required=False, default=None)
    query: str = Field(required=False)  # TODO: to be validated with Oxide
    arguments: list = Field(required=False, default_factory=list)
    parameters: dict = Field(required=False, default_factory=dict)
    retrieved: datetime = Field(required=False, default=datetime.utcnow())
    raw_result: bool = Field(default=False)
    queued: bool = Field(default=False)
    connection: Optional[Any] = Field(required=False)

    class Meta:
        strict = True


class QueryResult(BaseModel):
    driver: str = Field(required=False, default='pg')
    state: str = Field(required=False)
    query: str = Field(required=False, default=None)
    data: Union[list, dict] = Field(required=False, default_factory=list)
    duration: float = Field(required=False, default=None)
    errors: Optional[dict] = Field(required=False, default=None)

    class Meta:
        strict = True
