from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.models.procarts import ProCart
from app.db.models.products import Product
from app.db.models.carts import Cart

from app.db.scheme.procarts import PrCartCreate, PrCartUpdate

from typing import Optional

class PrCartCrud:

    @staticmethod
    async def cr_ca_get_id(db:AsyncSession, user_id:int) -> Optional[int]:
        cart=await db.execute(select(Cart.cart_id).filter(Cart.user_id==user_id))
        cart_id=cart.scalar_one_or_none()
        return cart_id
    
    
    @staticmethod
    async def cr_prcart_get_all(db:AsyncSession, cart_id: int) -> list[ProCart]:
        result = await db.execute(
            select(ProCart)
            .filter(ProCart.cart_id == cart_id)
            .options(selectinload(ProCart.product)) 
        )
        return result.scalars().all()
    

    @staticmethod
    async def cr_prcart_get_id(db:AsyncSession, pro_id:int, cart_id:int) -> ProCart:    
        result = await db.execute(
            select(ProCart)
            .filter(ProCart.pro_id == pro_id, ProCart.cart_id == cart_id)
            .options(selectinload(ProCart.product)))
    
        return result.scalars().one_or_none()
    

    @staticmethod
    async def cr_prcart_get_name(db:AsyncSession, cart_id:int, pro_name:str) -> list[ProCart]:
        result = await db.execute(
           select(ProCart).join(Product)
           .filter(ProCart.cart_id == cart_id, Product.pro_name.contains(pro_name))
           .options(selectinload(ProCart.product)))

        return result.scalars().all()


    @staticmethod
    async def cr_prcart_get_pro_id(db:AsyncSession, pro_id:int, cart_id:int) ->  Optional[ProCart]:
        result = await db.execute(
            select(ProCart)
            .filter(ProCart.pro_id == pro_id, ProCart.cart_id == cart_id)
            .options(selectinload(ProCart.product)))
    
        return result.scalars().one_or_none()
    

    @staticmethod
    async def cr_prcart_update_qty(db: AsyncSession, pro_cart_id: int, qty: int) -> ProCart:
        db_prcart = await db.get(ProCart, pro_cart_id, options=[selectinload(ProCart.product)])
        if db_prcart:
            db_prcart.qty = qty
            await db.flush()
        return db_prcart
    

    @staticmethod
    async def cr_prcart_create(db:AsyncSession, prcart: PrCartCreate) -> ProCart:
        new_prcart=ProCart(**prcart.model_dump())
        db.add(new_prcart)
        await db.flush()
        return new_prcart


    @staticmethod
    async def cr_prcart_update_by_id(db:AsyncSession, prcart:PrCartUpdate, 
                                     pro_cart_id:int) -> ProCart | None:
        
        prcart_data=await db.get(ProCart, pro_cart_id, options=[selectinload(ProCart.product)])
        if prcart_data:
            update_data=prcart.model_dump(exclude_unset=True)
            for key, Value in update_data.items():
                setattr(prcart_data,key, Value)
            await db.flush()

            return prcart_data
            
        return None
    
    @staticmethod
    async def cr_prcart_delete_by_id(db: AsyncSession, pro_cart_id: int) -> ProCart | None:
        db_prcart = await db.get(ProCart, pro_cart_id)
        if db_prcart:
            await db.delete(db_prcart)
            await db.flush()

            return db_prcart
            
        return None


    @staticmethod
    async def cr_prcart_delete_all(db: AsyncSession, cart_id: int) -> int:
        db_prcart = delete(ProCart).where(ProCart.cart_id == cart_id)

        result =await db.execute(db_prcart)
        await db.flush()

        return result.rowcount

    
