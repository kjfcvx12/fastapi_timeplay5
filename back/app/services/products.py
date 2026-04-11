from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.db.crud.products import PrCrud
from app.db.models.products import Product
from app.db.scheme.products import PrCreate, PrUpdate

class ProService:

    @staticmethod
    async def se_pr_get_all(db:AsyncSession) -> list[Product]:
        db_pro=await PrCrud.cr_pr_get_all(db)

        if not db_pro:
            raise HTTPException(status_code=404, 
                                detail="등록된 상품이 없습니다.")
        return db_pro
    

    @staticmethod
    async def se_pr_get_id(db:AsyncSession, pro_id:int) -> Product:
        db_pro=await PrCrud.cr_pr_get_by_id(db, pro_id)

        if not db_pro:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 id의 상품은 없습니다.")
        return db_pro


    @staticmethod
    async def se_pr_get_name(db:AsyncSession, pro_name:str)-> list[Product]:
        db_pro=await PrCrud.cr_pr_get_by_name(db, pro_name)

        if not db_pro:
            raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
        return db_pro



    @staticmethod
    async def se_pr_create(db:AsyncSession, product:PrCreate) ->Product:
        try:    
            db_pro=await PrCrud.cr_pr_create(db, product)
            await db.commit()
            await db.refresh(db_pro)
            return db_pro

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 등록 실패: {str(e)}")


    @staticmethod
    async def se_pr_update(db:AsyncSession, product:PrUpdate, pro_id:int)-> Product:
        try:
            db_pro=await PrCrud.cr_pr_update_by_id(db, product, pro_id)
            
            if not db_pro:
                raise HTTPException(status_code=404, 
                                    detail="찾으시는 id의 상품이 없습니다.")
            
            await db.commit()
            await db.refresh(db_pro)
            return db_pro
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 수정 실패: {str(e)}")

    
    @staticmethod
    async def se_pr_delete(db:AsyncSession, pro_id:int)-> Product:
        try:
            db_pro=await PrCrud.cr_pr_delete_by_id(db, pro_id)
            
            if not db_pro:
                raise HTTPException(status_code=404, 
                                    detail="찾으시는 id의 상품이 없습니다.")
            
            await db.commit()
            return db_pro
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 삭제 실패: {str(e)}")
