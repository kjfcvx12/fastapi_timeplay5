from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail

from app.db.scheme.orders import OrCreate, OrRead

class OrderCrud:

    @staticmethod
    async def cr_or_get_all(db:AsyncSession, order:OrRead) -> list[OrderDetail]:
        result=await db.execute(select(OrderDetail).
                                filter(OrRead.order_id==OrderDetail.order_id))
        return result.scalars().all()
    
    @staticmethod
    async def cr_ca_get_id(db:AsyncSession, order_id:str) -> list[OrderDetail]:
        result=await db.execute(select(Order).filter(Order.order_id==order_id))
        return result.scalars().one_or_none()