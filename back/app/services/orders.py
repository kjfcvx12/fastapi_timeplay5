from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail 

from app.db.models.carts import Cart
from app.db.models.products import Product

from app.db.scheme.orders import OrRead, OrCreate, OrUpdate
from app.db.scheme.orderdetails import OrDeRead, OrDeCreate 
from app.db.scheme.products import PrUpdate

from app.db.crud.orders import OrderCrud
from app.db.crud.orderdetails import OdCrud
from app.db.crud.procarts import PrCartCrud
from app.db.crud.products import PrCrud

from datetime import datetime

from typing import Optional


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
    async def se_order_create(db:AsyncSession, order:OrCreate, prcart:list) -> Order:

        try:

            db_order=await OrderCrud.cr_pr_create(db, order)
            
            for i in prcart:
                
                db_pro=await PrCrud.cr_pr_get_by_id(db,i.pro_id)
                
                if not db_pro or db_pro.qty < i.qty:
                    raise HTTPException(status_code=400, 
                                        detail=f"상품{i.pro_id} 재고가 부족합니다.")

                data = i.model_dump()
                data['order_id'] = db_order.order_id
                await OdCrud.cr_od_create(db,OrDeCreate(**data))

                  
                db_product=await PrCrud.cr_pr_update_qty(db, pro_id=i.pro_id, eqty=i.qty)

                db_prcart=await PrCartCrud.cr_prcart_delete_by_id(db, i, i.pro_id)


            await db.commit()
            await db.refresh(db_order)

            return db_order

        except HTTPException:
            await db.rollback()
            raise
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"주문 실패: {str(e)}")
    
    
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
    async def se_order_cancel(db: AsyncSession, order_id: int) -> Order:
        try:

            db_order=await OrderCrud.cr_or_get_order_id(db, order_id)
            if not db_order:
                raise HTTPException(status_code=404, detail="주문 정보를 찾을 수 없습니다.")
                
            od=await OdCrud.cr_od_get_id_all(db, order_id)
            
            for i in od:
                await PrCrud.cr_pr_update_qty(db, pro_id=i.pro_id, eqty=-i.qty) 

            update_data = {"order_state": 4} 
            await OrderCrud.cr_or_update_by_id(db, order_id, update_data)

            await db.commit()
            await db.refresh(db_order)
            return db_order

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"주문 취소 실패: {str(e)}")


    # 주문 조회 주문 id od
    @staticmethod
    async def se_order_get_od_id(db:AsyncSession, order_id:int)->list[OrderDetail]:
        db_od=await OdCrud.cr_od_get_id_all(db, order_id)

        if not db_od:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 주문이 없습니다.")
        return db_od
