from pydantic import BaseModel, Field

from typing import Optional

from app.db.scheme.products import PrRead

class PrCartBase(BaseModel):
    qty:int=Field(..., ge=09)

class PrCartCreate(PrCartBase):
    pro_id:int
    cart_id:int

class PrCartUpdate(PrCartBase):
    qty:Optional[int]=Field(None, ge=0)
    
class PrCartInDB(PrCartBase):
    pro_cart_id: int
    
    class Config:
        from_attributes = True

class PrCartRead(PrCartInDB):
    product: PrRead