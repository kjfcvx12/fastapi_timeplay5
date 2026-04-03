from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.procarts import ProCart
from app.db.scheme.procarts import PrCartCreate, PrCartUpdate


class PrCartCrud:

    @staticmethod
    async def cr_prcart_create(db:AsyncSession, procart:PrCartCreate) -> ProCart:
        new_procart=ProCart(**procart.model_dump())
        db.add(new_procart)
        await db.flush()
        return new_procart


    @staticmethod
    async def cr_prcart_update_by_id(db:AsyncSession, product:PrCartUpdate, 
                                     pro_cart_id:int) -> ProCart | None:
        
        prcart_data=await db.get(ProCart, pro_cart_id)
        if prcart_data:
            update_data=product.model_dump(exclude_unset=True)
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
