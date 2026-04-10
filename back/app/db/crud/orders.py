from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.products import Product
from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail

from app.db.scheme.orders import OrCreate, OrRead, OrUpdate



class OrderCrud:

    # 주문 전체 조회 관리자
    @staticmethod
    async def cr_or_get_all(db:AsyncSession) -> list[OrderDetail]:
        result=await db.execute(select(Order))
        return result.scalars().all()

    # 주문 전체 조회 유저
    @staticmethod
    async def cr_or_get_all_id(db:AsyncSession, order_id:int) -> list[OrderDetail]:
        result=await db.execute(select(OrderDetail).
                                filter(order_id==OrderDetail.order_id))
        return result.scalars().all()

    @staticmethod
    async def cr_or_update_state(db:AsyncSession, order_id:int, order_state:int) -> Order:
        db_order=await db.execute(select(OrderDetail).filter(order_id==OrderDetail.order_id))


    async def cr_or_update_by_id(db:AsyncSession, order:OrUpdate, 
                                 order_id:int) -> Order | None:        
        db_order=await db.get(Order, order_id)
        if db_order:
            update_data=Order.model_dump(exclude_unset=True)
            for key, Value in update_data.items():
                setattr(db_order,key, Value)
            await db.flush()

            return db_order
            
        return None