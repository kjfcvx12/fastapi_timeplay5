from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status

from app.db.crud.carts import CaCrud

from app.db.models.carts import Cart
from app.db.scheme.carts import CaRead, PrCartRead


class ProService:

    @staticmethod
    async def se_cart_get_all(db:AsyncSession) -> Cart:
        db_cart=await CaCrud.cr_ca_get_all(db, PrCartRead)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="등록된 상품이 없습니다.")
        return db_cart
    
    @staticmethod
    async def se_cart_get_name(db:AsyncSession, pro_name:str)->list[Cart]:
        db_cart=await CaCrud.cr_ca_get_name(db, pro_name)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_cart


    
