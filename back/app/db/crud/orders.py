from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.products import Product
from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail

from app.db.scheme.orders import OrCreate, OrRead



class OrderCrud:

    @staticmethod
    async def cr_or_get_all(db:AsyncSession, order_id:int) -> list[OrderDetail]:
        result=await db.execute(select(OrderDetail).
                                filter(order_id==OrderDetail.order_id))
        return result.scalars().all()

    @staticmethod
    async def cr_or_update_pro(db: AsyncSession, pro_id: int, pro_qty: int):
        result = await db.execute(select(Product).filter(Product.pro_id == pro_id))
        product = result.scalar_one_or_none()
        if product and product.qty >= pro_qty:
            product.qty -= pro_qty
            await db.flush()
            return True
        return False