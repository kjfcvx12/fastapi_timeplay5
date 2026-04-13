from pydantic import BaseModel, Field


from app.db.scheme.products import PrRead


class OrDeBase(BaseModel):
    qty:int=Field(..., ge=0)
    price:int=Field(..., ge=0)

class OrDeCreate(OrDeBase):
    pro_id: int
    order_id: int

class OrDeInDB(OrDeBase):
    od_id: int
    pro_id: int
    order_id: int
    
    class Config:
        from_attributes = True

class OrDeRead(OrDeInDB):
    product: PrRead