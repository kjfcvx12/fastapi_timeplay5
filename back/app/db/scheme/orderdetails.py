from pydantic import BaseModel, Field

from typing import Optional

from products import PrRead

class OrDeBase(BaseModel):
    qty:int=Field(..., ge=0)
    price:int=Field(..., ge=0)

class OrDeCreate(OrDeBase):
    pro_id:int
    cart_id:int
    price: int


class OrDeInDB(OrDeBase):
    od_id: int
    
    class Config:
        from_attributes = True

class OrDeRead(OrDeInDB):
    product: PrRead