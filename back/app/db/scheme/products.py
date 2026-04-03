from pydantic import BaseModel, Field

from typing import Optional

class PrBase(BaseModel):
    pro_name : str
    qty : int=Field(..., ge=0, le=99)
    price : int=Field(..., ge=0)

class PrCreate(PrBase):
    pass

class PrUpdate(BaseModel):
    pro_name : str | None=None
    qty : Optional[int]=Field(None, ge=0, le=99)
    price : Optional[int]=Field(None, ge=0)

class PrInDB(PrBase):
    pro_id: int

    class Config:
        from_attributes = True

class PrRead(PrInDB):
    pass