from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from app.db.models.orderdetails import OrderDetail
from app.db.models.products import Product

from app.db.scheme.orderdetails import OrDeRead, OrDeCreate



class OdCrud:

    # 주문 조회 주문 id od
    @staticmethod
    async def cr_od_get_id_all(db:AsyncSession, order_id:int) -> list[OrderDetail]:
        result=await db.execute(select(OrderDetail)
                                .filter(OrderDetail.order_id==order_id)
                                .options(selectinload(OrderDetail.product)))
        return result.scalars().all()
    
    @staticmethod
    async def cr_od_get_id(db:AsyncSession, od_id:int) -> OrderDetail | None:
        result=await db.execute(select(OrderDetail)
                                .filter(OrderDetail.od_id==od_id))
        return result.scalar_one_or_none()

    
    # 주문 상세 생성 장바구니에서 선택한 상품으로 주문 생성
    @staticmethod
    async def cr_od_create(db:AsyncSession, od:OrDeCreate) -> OrderDetail:
        new_OrderDetail=OrderDetail(**od.model_dump())
        db.add(new_OrderDetail)
        await db.flush()
        return new_OrderDetail
    

        







