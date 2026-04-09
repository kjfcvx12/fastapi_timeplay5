from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status

from app.db.crud.carts import CaCrud
from app.db.crud.procarts import PrCartCrud, PrCartUpdate, PrCartCreate

from app.db.models.carts import Cart
from app.db.models.procarts import ProCart 

from typing import Optional


class CartService:

    @staticmethod
    async def se_cart_get_cart_id(db:AsyncSession, user_id:int) -> Optional[int]:
        db_cart=await PrCartCrud.cr_ca_get_id(db,user_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니가 없습니다.")
        return db_cart

    @staticmethod
    async def se_cart_get_all(db:AsyncSession, user_id:int) -> list[ProCart]:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)
        
        db_procart=await PrCartCrud.cr_prcart_get_all(db, cart_id)

        if not db_procart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 담긴 상품이 없습니다.")
        return db_procart
    
    @staticmethod
    async def se_prcart_get_pro_id(db:AsyncSession, user_id:int, pro_id:int)->ProCart:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)

        db_cart=await PrCartCrud.cr_prcart_get_id(db, pro_id, cart_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 찾으시는 id의 상품은 없습니다.")
        return db_cart
    
    @staticmethod
    async def se_cart_get_name(db:AsyncSession, user_id:int, pro_name:str)->list[ProCart]:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)

        db_cart=await PrCartCrud.cr_prcart_get_name(db, pro_name, cart_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 찾으시는 이름의 상품은 없습니다.")
        return db_cart


# cart 상품 추가시 상품이 존재하면 수정, 아니면 추가
    @staticmethod
    async def se_add_or_update(db: AsyncSession, user_id: int, 
                               prcart:PrCartCreate) -> ProCart:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)

        pro = await PrCartCrud.cr_prcart_get_id_pro_id(db, cart_id, prcart.pro_id)

        if pro:
            new_qty = pro.qty + prcart.qty
            return await PrCartCrud.cr_prcart_update_qty(db, pro.pro_cart_id, new_qty)

        return await PrCartCrud.cr_prcart_create(db, prcart)

# 상품 수량 변경
    @staticmethod
    async def se_prcart_update(db:AsyncSession, prcart:PrCartUpdate, pro_cart_id:int) -> ProCart | None:
        db_prcart=await PrCartCrud.cr_prcart_update_by_id(db, prcart, pro_cart_id)

        if not db_prcart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 찾으시는 이름의 상품은 없습니다.")
        return db_prcart

# 상품 삭제
    @staticmethod
    async def se_prcart_delete(db:AsyncSession, pro_cart_id:int, user_id:int) -> ProCart | None:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)
        
        db_prcart=await PrCartCrud.cr_prcart_delete_by_id(db, pro_cart_id)

        if not db_prcart:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_prcart


# 상품 전부 지우기
    @staticmethod
    async def se_ca_delete(db:AsyncSession, user_id:int)->Cart|None:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)
        
        db_cart=await PrCartCrud.cr_cart_delete_by_id(db, cart_id)
        
        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 상품이 없습니다.")
        
        return db_cart


    
