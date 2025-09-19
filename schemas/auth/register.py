from pydantic import BaseModel, EmailStr, Field



class UserRegister(BaseModel):
    login: str
    email: EmailStr
    password: str

