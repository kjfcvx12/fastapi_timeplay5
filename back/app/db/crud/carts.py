from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.db.models.carts import Cart
from app.db.scheme.carts import CaCreate

class CaCrud:

    @staticmethod
    async def cr_ca_create(db:AsyncSession, cart:CaCreate) -> Cart:
        new_cart=Cart(**cart.model_dump())
        db.add(new_cart)
        await db.flush()
        return new_cart
   
    

    

    