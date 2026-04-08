from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.reviews import Review
from app.db.scheme.reviews import ReviewCreate, ReviewUpdate


#DB의 reviews 테이블에 데이터를 넣고 빼는 것
class ReviewCrud:

    #리뷰 작성
    @staticmethod
    async def cr_re_create(db:AsyncSession, review:ReviewCreate) -> Review:
        db_review=Review(**review.model_dump())
        db.add(db_review)
        await db.flush()
        return db_review
    
    #리뷰 수정(리뷰 아이디로 수정)
    @staticmethod
    async def cr_re_update(db:AsyncSession, rev_id:int, review:ReviewUpdate) -> Review | None:
        db_review=await db.get(Review, rev_id)

        if db_review:
            update_data=review.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_review, key, value)
            await db.flush()
            return db_review
        return None
    
    #리뷰 삭제(리뷰 아이디로 삭제)
    @staticmethod
    async def cr_re_delete(db:AsyncSession, rev_id:int) -> Review | None:
        db_review=await db.get(Review, rev_id)

        if db_review:
            await db.delete(db_review)
            await db.flush()
            return db_review
        return None
    
    #리뷰 조회

    #rev_id
    @staticmethod
    async def cr_re_get_rev_id(db:AsyncSession, rev_id:int) -> Review | None:
        result=await db.execute(select(Review).filter(Review.rev_id == rev_id))
        return result.scalar_one_or_none()
    
    #pro_id 모든 리뷰
    @staticmethod
    async def cr_re_get_pro_id(db:AsyncSession, pro_id:int) -> list[Review]:
        result=await db.execute(select(Review).filter(Review.pro_id == pro_id))
        return result.scalars().all()   

    #user_id 모든 리뷰
    @staticmethod
    async def cr_re_get_user_id(db:AsyncSession, user_id:int) -> list[Review]:
        result=await db.execute(select(Review).filter(Review.user_id == user_id))
        return result.scalars().all()

    #전체 리뷰
    @staticmethod
    async def cr_re_get_all(db:AsyncSession):
        result=select(Review)
        result2=await db.execute(result)
        return result2.scalars().all()


