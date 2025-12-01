from typing import Annotated
from fastapi import HTTPException, Query, status
from pydantic import BaseModel, Field, ValidationError


class Pagination(BaseModel):
    total: int = None
    page: int = Field(default=0, gt=0)
    size: int = Field(default=20, gt=0, le=100)

    @classmethod
    def as_query(
        cls,
        page: Annotated[int, Query()],
        size: Annotated[int, Query()]
        ) -> 'Pagination':
        try:
            return cls(
                page=page,
                size=size
            )
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    'detail' : error.errors(
                        include_context=False,
                        include_input=False,
                        include_url=False
                    )
                }
            )

# class PaginationQuery(BaseModel):
#     page: int = Field(default=0, gt=0)
#     size: int = Field(default=20, gt=0, le=100)


