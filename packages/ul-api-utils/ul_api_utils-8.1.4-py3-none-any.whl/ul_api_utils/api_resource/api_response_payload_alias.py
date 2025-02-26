from datetime import datetime
from types import NoneType

from pydantic import UUID4, RootModel

from ul_api_utils.api_resource.api_response import JsonApiResponsePayload


class ApiBaseModelPayloadResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime
    is_alive: bool


class ApiBaseUserModelPayloadResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime
    user_created_id: UUID4
    user_modified_id: UUID4
    is_alive: bool


class ApiEmptyResponse(RootModel[NoneType]):  # type: ignore
    pass
