from pydantic import BaseModel, Field
from datetime import datetime,timezone
from typing import Annotated


class Userbase(BaseModel):
    user_name: str
    email: str
    address: str
    phone: str
    
class UserCreate(BaseModel):
    user_name: str
    email: str
    pw: Annotated[str, Field(max_length=72)]
    address: str
    phone: str

class UserLogin(BaseModel):
    email: str
    pw: Annotated[str, Field(max_length=72)]

class UserUpdate(BaseModel):
    email: str | None = None
    user_name: str | None = None
    pw: str | None = None
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
