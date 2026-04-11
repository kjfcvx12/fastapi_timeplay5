from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select


from app.db.models.products import Product
from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail

from app.db.scheme.orders import OrCreate, OrRead, OrUpdate

from datetime import datetime

class OrderCrud:

    # 주문 전체 조회 관리자
    @staticmethod
    async def cr_or_get_all(db:AsyncSession) -> list[Order]:
        result=await db.execute(select(Order))
        return result.scalars().all()

    # 주문 전체 조회 유저
    @staticmethod
    async def cr_or_get_id(db:AsyncSession, user_id:int) -> list[Order]:
        result=await db.execute(select(Order).
                                filter(user_id==Order.user_id))
        return result.scalars().all()
    
    # 주문 조회 날짜 order
    @staticmethod
    async def cr_or_get_date(db:AsyncSession, ordered_at:datetime) -> list[Order]:
        result=await db.execute(select(Order).
                                filter(ordered_at==Order.ordered_at))
        return result.scalars().all()
    
    # 주문 조회 order_id
    @staticmethod
    async def cr_or_get_order_id(db:AsyncSession, order_id:int) -> Order:
        result=await db.execute(select(Order).
                                filter(order_id==Order.order_id).
                                options(selectinload(Order.orderdetails)))
        return result.scalars().one_or_none()

    # 주문 생성
    @staticmethod
    async def cr_pr_create(db:AsyncSession, order:OrCreate) -> Order:
        new_order=Order(**order.model_dump())
        db.add(new_order)
        await db.flush()
        return new_order


    # 주문 상태 수정
    @staticmethod
    async def cr_or_update_by_id(db:AsyncSession, order:OrUpdate, 
                                 order_id:int) -> Order | None:        
        db_order=await db.get(Order, order_id)
        if db_order:
            update_data=order.model_dump(exclude_unset=True)
            for key, Value in update_data.items():
                setattr(db_order,key, Value)
            await db.flush()

            return db_order
            
        return None
    
    # 주문 삭제
    @staticmethod
    async def cr_or_delete_by_id(db: AsyncSession, order_id: int) -> Order | None:
        db_order = await db.get(Order, order_id)
        if db_order:
            await db.delete(db_order)
            await db.flush()

            return db_order
            
        return None