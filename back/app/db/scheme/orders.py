from pydantic import BaseModel, Field
from typing import List

from orderdetails import OrDeRead

class OrBase(BaseModel):
    total : int=Field(..., ge=0)
    pay : int=Field(..., ge=0, le=1)
    order_state: int=Field(..., ge=0, le=4)
    user_id:int=Field(...)

class OrCreate(OrBase):
    pass


class OrInDB(OrBase):
    order_id:int

    class Config:
        from_attributes=True

class OrRead(OrInDB):
    orderdetails:List[OrDeRead]=[]