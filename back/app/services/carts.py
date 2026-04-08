from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status

from app.db.crud.carts import CaCrud
from app.db.crud.procarts import PrCartCrud, PrCartUpdate

from app.db.models.carts import Cart
from app.db.models.procarts import ProCart 


class CartService:

    @staticmethod
    async def se_cart_get_all(db:AsyncSession, user_id: int) -> list[ProCart]:
        db_cart=await PrCartCrud.cr_prcart_get_all(db, user_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 담긴 상품이 없습니다.")
        return db_cart
    
    @staticmethod
    async def se_cart_get_id(db:AsyncSession, user_id:int, pro_cart_id:int)->list[ProCart]:
        db_cart=await PrCartCrud.cr_prcart_get_id(db, user_id, pro_cart_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_cart
    
    @staticmethod
    async def se_cart_get_name(db:AsyncSession, user_id:int, pro_name:str)->list[ProCart]:
        db_cart=await PrCartCrud.cr_prcart_get_name(db, user_id, pro_name)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_cart


# cart 상품 추가시 상품이 존재하면 수정, 아니면 추가
    @staticmethod
    async def se_add_or_update_product(db: AsyncSession, user_id: int, product: any) -> ProCart:

        pro = await PrCartCrud.cr_prcart_get_id_pro_id(db, user_id, product.pro_id)

        if pro:
            new_qty = pro.qty + product.qty
            return await PrCartCrud.cr_prcart_update_qty(db, pro.pro_cart_id, new_qty)

        return await PrCartCrud.cr_prcart_create(db, product)

# 상품 수량 변경
    @staticmethod
    async def se_prcart_update(db:AsyncSession, prcart:PrCartUpdate, pro_cart_id:int) -> ProCart | None:
        db_prcart=await PrCartCrud.cr_prcart_update_by_id(db, prcart, pro_cart_id)

        if not db_prcart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_prcart

# 상품 삭제
    @staticmethod
    async def se_prcart_delete(db:AsyncSession, pro_cart_id:int) -> ProCart | None:
        db_prcart=await PrCartCrud.cr_prcart_delete_by_id(db, pro_cart_id)

        if not db_prcart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_prcart


# 상품 전부 지우기
    @staticmethod
    async def se_ca_delete(db:AsyncSession)->Cart|None:
        await CaCrud.cr_ca_delete(db)

        return True


    
