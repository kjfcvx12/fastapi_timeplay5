from pydantic import BaseModel, Field


class CaBase(BaseModel):
    user_id:int=Field(...)

class CaCreate(CaBase):
    pass

class CaInDB(CaBase):
    cart_id: int

    class Config:
        from_attributes=True

class CaRead(CaInDB):
    pass