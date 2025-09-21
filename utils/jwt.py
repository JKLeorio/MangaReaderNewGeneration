import jwt
import logging

from typing import Any, Dict

from pydantic import ValidationError



from schemas.auth.payload import Payload
from settings import (
    SECRET, 
    TOKEN_ALGORITHM
    )


logger = logging.getLogger(__name__)


def generate_jwt(payload: Dict[str, Any]) -> str:
    """
    param: payload must be dict with values that can be converted to json format
    return: jwt token
    """
    jwt_token = jwt.encode(
        payload=payload,
        key=SECRET,
        algorithm=TOKEN_ALGORITHM
        )
    return jwt_token

def decode_jwt(token: str) -> dict[str, Any]:
    """
    param: token -> jwt token
    decode jwt, then return payload
    """
    payload = jwt.decode(jwt=token, key=SECRET, algorithms=TOKEN_ALGORITHM)
    return payload


def validate_jwt(token: str) -> None | Payload:
    """
    param: token -> jwt token
    return: payload
    decode, validate jwt token, then return payload
    """
    payload = None
    try:
        payload = decode_jwt(token=token)
        try:
            payload = Payload.model_validate(payload)
        except ValidationError:
            return payload
    except jwt.exceptions.DecodeError as error:
        logger.exception(msg=error)
    finally:
        return payload

