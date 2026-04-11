from pydantic import BaseModel, Field


class PrBase(BaseModel):
    pro_name : str
    qty : int=Field(..., ge=0)
    price : int=Field(..., ge=0)

class PrCreate(PrBase):
    pass

class PrUpdate(BaseModel):
    pro_name: str | None = None
    qty: int | None = Field(None, ge=0)
    price: int | None = Field(None, ge=0)

class PrInDB(PrBase):
    pro_id: int

    class Config:
        from_attributes = True

class PrRead(PrInDB):
    pass