from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models.orderdetails import OrderDetail
from app.db.models.products import Product

from app.db.scheme.orderdetails import OrDeRead, OrDeCreate



class OdCrud:

    @staticmethod
    async def cr_od_get_all(db:AsyncSession, order_id:int) -> list[OrderDetail]:
        result=await db.execute(select(OrderDetail).filter(OrderDetail.order_id==order_id))
        return result.scalars().all()
    

    @staticmethod
    async def cr_od_get_name(db:AsyncSession, order_id:int, pro_name:str) -> list[OrderDetail]:
        ids=await db.execute(select(Product.pro_id).filter(Product.pro_name.contains(pro_name)))
        od_ids=ids.scalars().all()

        if not od_ids:
            return []

        result=await db.execute(select(OrderDetail)
                                .filter(OrderDetail.order_id == order_id,
                                OrderDetail.pro_id.in_(od_ids)))
        return result.scalars().all()
    

    @staticmethod
    async def cr_od_create(db:AsyncSession, od:OrDeCreate) -> OrderDetail:
        new_OrderDetail=OrderDetail(**od.model_dump())
        db.add(new_OrderDetail)
        await db.flush()
        return new_OrderDetail
        

    @staticmethod
    async def cr_od_delete_by_id(db: AsyncSession, od_id: int) -> OrderDetail | None:
        db_od = await db.get(OrderDetail, od_id)
        if db_od:
            await db.delete(db_od)
            await db.flush()

            return db_od
        
        return None
