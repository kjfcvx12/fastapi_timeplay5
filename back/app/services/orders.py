from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail 

from app.db.models.carts import Cart
from app.db.models.products import Product

from app.db.scheme.orders import OrRead, OrCreate, OrUpdate
from app.db.scheme.orderdetails import OrDeRead, OrDeCreate 
from app.db.scheme.procarts import PrCartRead

from app.db.crud.orders import OrderCrud
from app.db.crud.orderdetails import OdCrud
from app.db.crud.procarts import PrCartCrud
from app.db.crud.products import PrCrud

from datetime import datetime


class OrService:
    # 주문 조회 전체 order
    @staticmethod
    async def se_order_get_all(db:AsyncSession) -> list[Order]:
        db_order=await OrderCrud.cr_or_get_all(db)

        if not db_order:
            raise HTTPException(status_code=404, 
                                detail="주문이 없습니다.")
        return db_order


    # 주문 조회 유저 주문 전체 order
    @staticmethod
    async def se_order_get_id(db:AsyncSession, user_id:int) -> list[Order]:
        db_order=await OrderCrud.cr_or_get_id(db, user_id)

        if not db_order:
            raise HTTPException(status_code=404, 
                                detail="해당 유저의 주문이 없습니다.")
        return db_order


    # 주문 조회 날짜 order
    @staticmethod
    async def se_order_get_date(db:AsyncSession, ordered_at:datetime) -> list[Order]:
        db_order=await OrderCrud.cr_or_get_date(db, ordered_at)

        if not db_order:
            raise HTTPException(status_code=404, 
                                detail="해당 날짜의 주문이 없습니다.")
        return db_order


    # 주문 생성 order
    @staticmethod
    async def se_order_create(db:AsyncSession, order:OrCreate, prcart:list[PrCartRead], user_id:int) -> Order:
        # try:
            if not isinstance(prcart, list):
                prcart = [prcart]

            order_data=order.model_dump(exclude={'pro', 'user_id','total'})
            order_data['user_id']=user_id
            order_data['total'] = 0
            db_order=await OrderCrud.cr_or_create(db, order_data)
            
            total=0
            for i in prcart:
                
                db_pro=await PrCrud.cr_pr_get_by_id(db, i.pro_id)
                
                if not db_pro or db_pro.qty < i.qty:
                    raise HTTPException(status_code=400, 
                                        detail=f"상품{i.pro_id} 재고가 부족합니다.")
                
                od_data = {"order_id": db_order.order_id, 
                           "pro_id": i.pro_id, 
                           "qty": i.qty, 
                           "price": db_pro.price}
                await OdCrud.cr_od_create(db, OrDeCreate(**od_data))
                new_total=i.qty*db_pro.price
                total+=new_total
                
                await PrCrud.cr_pr_update_qty(db, pro_id=i.pro_id, eqty=i.qty)

                await PrCartCrud.cr_prcart_delete_by_id(db, i.pro_cart_id)
                
            
            update_data={"total": total}
            await OrderCrud.cr_or_update_by_id(db, update_data, db_order.order_id)

            await db.commit()
            await db.refresh(db_order, ['orderdetails'])
            return db_order


        # except HTTPException:
        #     await db.rollback()
        #     raise
        
        # except Exception as e:
        #     await db.rollback()
        #     raise HTTPException(status_code=500, 
        #                         detail=f"주문 실패: {str(e)}")
    
    
    # 주문 수정 상태 수정 관리자 order
    @staticmethod
    async def se_order_update(db:AsyncSession, order:OrUpdate, order_id:int) -> Order|None:
        try:
            db_order=await OrderCrud.cr_or_update_by_id(db, order, order_id)
            
            if not db_order:
                raise HTTPException(status_code=404, 
                                    detail="찾으시는 id의 주문이 없습니다.")
            
            await db.commit()
            await db.refresh(db_order)
            return db_order
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"주문 수정 실패: {str(e)}")


    # 주문 취소 order
    @staticmethod
    async def se_order_cancel(db: AsyncSession, order_id: int, user_id:int) -> Order:
        try:
            db_user=await OrderCrud.cr_or_get_id(db,user_id)

            if not db_user:
                raise HTTPException(status_code=404, detail="해당 사용자의 주문이 없습니다.")

            db_order=await OrderCrud.cr_or_get_order_id(db, order_id)

            if not db_order:
                raise HTTPException(status_code=404, detail="주문 정보를 찾을 수 없습니다.")
            
            if db_order.user_id != user_id:
                raise HTTPException(status_code=403, detail="본인의 주문만 취소할 수 있습니다.")
                
            od=await OdCrud.cr_od_get_id_all(db, order_id)
            
            for i in od:
                await PrCrud.cr_pr_update_qty(db, pro_id=i.pro_id, eqty=-i.qty) 

            update_data = {"order_state": 4} 
            await OrderCrud.cr_or_update_by_id(db, update_data, order_id)

            await db.commit()
            await db.refresh(db_order)
            return db_order
        
        except HTTPException:
            await db.rollback()
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"주문 취소 실패: {str(e)}")


    # 주문 조회 주문 id order_id
    @staticmethod
    async def se_order_get_order_id(db:AsyncSession, order_id:int, user_id:int)->list[OrderDetail]:
        
        db_user=await OrderCrud.cr_or_get_id(db,user_id)

        if not db_user:
            raise HTTPException(status_code=404, detail="사용자가 일치 하지 않습니다.")

        db_od=await OdCrud.cr_od_get_id_all(db, order_id)

        if not db_od:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 주문이 없습니다.")
        return db_od
