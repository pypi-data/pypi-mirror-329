from datetime import date, datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_validator
from typing import Literal, Optional, Tuple, Any
from uuid import UUID

from maleo_core.utils.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class Base:
    #* ----- ----- Token ----- ----- *#
    class TokenPayload(BaseModel):
        uuid:UUID
        scope:Literal["refresh", "access"]
        iat:datetime
        exp:datetime

        @model_validator(mode="before")
        def set_iat_and_exp(cls, values:dict):
            iat = values.get("iat", None)
            exp = values.get("iat", None)
            if not iat and not exp:
                iat = datetime.now(timezone.utc)
                values["iat"] = iat
                if values["scope"] == "refresh":
                    values["exp"] = iat + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["scope"] == "access":
                    values["exp"] = iat + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            return values

    #* ----- ----- Authorization ----- ----- *#
    class ValidateResult(BaseModel):
        authorized:Literal[False, True]
        response:Optional[JSONResponse] = None
        token:Optional[str] = None

        class Config:
            arbitrary_types_allowed = True

    #* ----- ----- Base Parameters ----- ----- *#
    class GetParameters(BaseModel):
        date_filters: dict[
            Literal["created_at", "updated_at"],
            Tuple[
                Optional[date],
                Optional[date]
            ]
        ]
        sort_by:Literal["id", "created_at", "updated_at"]
        sort_order:Literal["asc", "desc"]
        page:int
        limit:int

    class Pagination(BaseModel):
        page_number:int
        data_count:int
        total_data:int
        total_pages:int

    class SingleQueryResult(BaseModel):
        data:Optional[Any]

    class MultipleQueryResult(BaseModel):
        data:list[Any]
        data_count:int
        total_data:int

    class SingleDataResult(BaseModel):
        data:Optional[Any]

    class MultipleDataResult(BaseModel):
        data:list[Any]
        pagination:Optional['Base.Pagination']

    class ControllerResult(BaseModel):
        success:Literal[True, False]
        response:Optional[JSONResponse]

        class Config:
            arbitrary_types_allowed=True

Base.Pagination.model_rebuild()
Base.MultipleDataResult.model_rebuild()