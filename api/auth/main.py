from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/form_login')


class TokenResponse(BaseModel):
    access_token: str