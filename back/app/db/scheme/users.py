from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,timezone
from typing import Annotated


class Userbase(BaseModel):
    user_name: str
    email: EmailStr
    address: str
    phone: str
    
class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    pw: Annotated[str, Field(max_length=72)]
    address: str
    phone: str

class UserLogin(BaseModel):
    email: EmailStr
    pw: Annotated[str, Field(max_length=72)]

class UserUpdate(BaseModel):
    pw: Annotated[str, Field(max_length=72, default=None)] 
    user_name: str | None = None    
    address: str | None = None
    phone: str | None = None

class UserInDB(Userbase):
    user_id: int
    role: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class UserRead(UserInDB):
    pass
