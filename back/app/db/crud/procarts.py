from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.procarts import ProCart
from app.db.models.products import Product
from app.db.models.users import Cart

from app.db.scheme.procarts import PrCartCreate, PrCartUpdate

from typing import Optional

class PrCartCrud:

    
    @staticmethod
    async def cr_prcart_get_all(db:AsyncSession, user_id:int) -> list[ProCart]:
        cart=await db.execute(select(Cart.cart_id).filter(Cart.user_id==user_id))
        cart_id=cart.scalar_one_or_none()

        if not cart_id:
            return []
        
        result=await db.execute(select(ProCart).filter(ProCart.cart_id==cart_id))
        return result.scalars().all()
    
    @staticmethod
    async def cr_prcart_get_id(db:AsyncSession, pro_cart_id:int, cart_id:int) -> ProCart:
        query = select(ProCart).filter(
            ProCart.pro_cart_id == pro_cart_id,
            ProCart.cart_id == cart_id)
    
        result = await db.execute(query)
    
        return result.scalars().one_or_none()

    @staticmethod
    async def cr_prcart_get_id_pro_id(db:AsyncSession, cart_id:int, pro_cart_id:int) ->  Optional[ProCart]:
        db_prcart = select(ProCart).filter(
            ProCart.pro_cart_id == pro_cart_id,
            ProCart.cart_id == cart_id)
    
        result = await db.execute(db_prcart)
    
        return result.scalars().one_or_none()
    
    @staticmethod
    async def cr_prcart_update_qty(db: AsyncSession, pro_cart_id: int, qty: int) -> ProCart:
        db_prcart = await db.get(ProCart, pro_cart_id)
        if db_prcart:
            db_prcart.qty = qty
            await db.flush()
        return db_prcart


    @staticmethod
    async def cr_prcart_get_name(db:AsyncSession, cart_id:int, pro_name:str) -> list[ProCart]:
        ids=await db.execute(select(Product.pro_id).filter(Product.pro_name.contains(pro_name)))
        pro_ids=ids.scalars().all()

        if not pro_ids:
            return []

        result=await db.execute(select(ProCart).filter(ProCart.cart_id == cart_id,
                                                       ProCart.pro_id.in_(pro_ids)))
        return result.scalars().all()
    

    @staticmethod
    async def cr_prcart_create(db:AsyncSession, product: any) -> ProCart:
        new_procart=ProCart(**product.model_dump())
        db.add(new_procart)
        await db.flush()
        return new_procart


    @staticmethod
    async def cr_prcart_update_by_id(db:AsyncSession, prcart:PrCartUpdate, 
                                     pro_cart_id:int) -> ProCart | None:
        
        prcart_data=await db.get(ProCart, pro_cart_id)
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
    
