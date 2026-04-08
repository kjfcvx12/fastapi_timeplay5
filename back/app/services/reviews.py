from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.reviews import Review
from app.db.scheme.reviews import ReviewCreate, ReviewUpdate
from sqlalchemy.future import select
from app.db.crud.reviews import ReviewCrud
from fastapi import HTTPException
from app.db.models.orderdetails import OrderDetail
from app.db.models.orders import Order




class ReviewService:
    #리뷰 작성(주문 여부)
    @staticmethod
    async def se_re_create(db:AsyncSession, user_id:int, review:ReviewCreate):
        result=await db.execute(select(OrderDetail)
        .join(
            Order, OrderDetail.order_id == Order.order_id
        )
        .where(
            OrderDetail.od_id == review.od_id,
            Order.user_id == user_id 
        ))
        order=result.scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=403, detail="본인 주문만 리뷰 작성 가능합니다")

        if order.pro_id != review.pro_id:
            raise HTTPException(status_code=400, detail="상품 정보가 일치하지 않습니다")
    
        
        create_review=await ReviewCrud.cr_re_create(db, review)
        create_review.user_id=user_id
        await db.commit()
        await db.refresh(create_review)

        return create_review
    
        
    #리뷰 수정
    @staticmethod
    async def se_re_update(db:AsyncSession, user_id:int, rev_id:int, review:ReviewUpdate):
        db_review=await ReviewCrud.cr_re_get_rev_id(db, rev_id)

        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰가 없습니다")

        if db_review.user_id != user_id:
            raise HTTPException(status_code=403, detail="본인만 수정이 가능합니다")

        update_review=await ReviewCrud.cr_re_update(db, rev_id, review)
        await db.commit()
        await db.refresh(update_review)

        return update_review      

    #리뷰 삭제
    @staticmethod
    async def se_re_delete(db:AsyncSession, user_id:int, rev_id:int):
        db_review=await ReviewCrud.cr_re_get_rev_id(db, rev_id)

        if not db_review:
            raise HTTPException(status_code=404, detail="리뷰가 없습니다")
        
        if db_review.user_id != user_id:
            raise HTTPException(status_code=403, detail="본인만 삭제가 가능합니다")
        
        await ReviewCrud.cr_re_delete(db, rev_id)
        await db.commit()

        return {"message" : "삭제가 완료되었습니다"}