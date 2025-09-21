from pydantic import BaseModel, EmailStr, Field



class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

