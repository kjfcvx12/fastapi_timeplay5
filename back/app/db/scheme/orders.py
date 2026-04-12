from pydantic import BaseModel, Field
from typing import List, Optional

from app.db.scheme.orderdetails import OrDeRead

class OrBase(BaseModel):
    total : int=Field(..., ge=0)
    pay : int=Field(..., ge=0, le=1)
    order_state: int=Field(..., ge=0, le=4)
    user_id:int=Field(...)

class OrCreate(BaseModel):
    user_id: int
    pay: int

class OrUpdate(BaseModel):
    order_state: Optional[int]=Field(None, ge=0, le=4)

class OrInDB(OrBase):
    order_id:int

    class Config:
        from_attributes=True

class OrRead(OrInDB):
    orderdetails:List[OrDeRead]=[]