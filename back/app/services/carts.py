from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status

from app.db.crud.carts import CaCrud

from app.db.models.carts import Cart
from app.db.models.procarts import ProCart 


class CartService:

    @staticmethod
    async def se_cart_get_all(db:AsyncSession, cart_id: int) -> list[ProCart]:
        db_cart=await CaCrud.cr_ca_get_all(db, cart_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 담긴 상품이 없습니다.")
        return db_cart
    
    @staticmethod
    async def se_cart_get_name(db:AsyncSession, cart_id:int, pro_name:str)->list[ProCart]:
        db_cart=await CaCrud.cr_ca_get_name(db, cart_id, pro_name)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_cart

# 상품이 장바구니에 있을 때 수정, 없을때 추가
    
