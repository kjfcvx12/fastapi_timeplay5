from pydantic import BaseModel, Field
from typing import List, Optional

from app.db.scheme.orderdetails import OrDeRead

class OrBase(BaseModel):
    pay : int=Field(..., ge=0, le=1)
    user_id:int|None

class CartPro(BaseModel):
    pro_id: int|None
    order_id: int|None
    qty: int|None
    price:int|None

class OrCreate(OrBase):
    total: int|None
    pro:List[CartPro] 

class OrUpdate(BaseModel):
    order_state: Optional[int]=Field(None, ge=0, le=4)

class OrInDB(OrBase):
    order_id:int
    total: int = Field(..., ge=0)
    order_state: int = Field(..., ge=0, le=4)

    class Config:
        from_attributes=True

class OrRead(OrInDB):
    orderdetails:List[OrDeRead]=[]
