from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator

from utils.datetime_utils import get_current_time


class PayloadBase(BaseModel):
    id: int
    login: str
    email: str
    expire_at: datetime

class Payload(PayloadBase):
    
    @field_validator("expire_at", mode="after")
    def is_token_expired(expire_at: datetime):
        now = get_current_time()
        if now >= expire_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='token is expired'
                )
        return expire_at