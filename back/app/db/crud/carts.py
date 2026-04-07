from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.carts import Cart
from app.db.models.procarts import ProCart
from app.db.models.products import Product
from app.db.scheme.carts import CaRead, PrCartRead, CaCreate

class CaCrud:

    @staticmethod
    async def cr_ca_get_all(db:AsyncSession, cart:CaRead) -> list[ProCart]:
        result=await db.execute(select(ProCart).filter(CaRead.cart_id==ProCart.cart_id))
        return result.scalars().all()
    
    @staticmethod
    async def cr_ca_get_name(db:AsyncSession, pro_name:str) -> list[ProCart]:
        ids=await db.execute(select(Product.pro_id).filter(Product.pro_name.contains(pro_name)))
        pro_ids=ids.scalars().all()

        if not pro_ids:
            return []

        result=await db.execute(select(ProCart).filter(ProCart.pro_id.in_(pro_ids)))
        return result.scalars().all()
    
    @staticmethod
    async def cr_ca_create(db:AsyncSession, cart:CaCreate) -> Cart:
        new_cart=Cart(**CaCreate.model_dump())
        db.add(new_cart)
        await db.flush()
        return new_cart
    