from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models.products import Product
from app.db.scheme.products import PrCreate, PrUpdate


class PrCrud:

    @staticmethod
    async def cr_pr_get_all(db:AsyncSession) -> list[Product]:
        result=await db.execute(select(Product))
        return result.scalars().all()
    

    @staticmethod
    async def cr_pr_get_by_id(db:AsyncSession, pro_id:int) -> Product:
        return await db.get(Product, pro_id)
    

    @staticmethod
    async def cr_pr_get_by_name(db:AsyncSession, pro_name:str) -> list[Product]:
        result=await db.execute(select(Product).filter(Product.pro_name.contains(pro_name)))
        return result.scalars().all()
    

    @staticmethod
    async def cr_pr_create(db:AsyncSession, product:PrCreate, role:str) -> Product:
        if role!="admin":
            return None
        
        new_product=Product(**product.model_dump())
        db.add(new_product)
        await db.flush()
        return new_product
        

    @staticmethod
    async def cr_pr_update_by_id(db:AsyncSession, product:PrUpdate, 
                                 pro_id:int, role:str) -> Product | None:
        if role!="admin":
            return None
        
        db_pro=await db.get(Product, pro_id)
        if db_pro:
            update_data=product.model_dump(exclude_unset=True)
            for key, Value in update_data.items():
                setattr(db_pro,key, Value)
            await db.flush()

            return db_pro
            
        return None
        

    @staticmethod
    async def cr_pr_delete_by_id(db: AsyncSession, pro_id: int, role:str) -> Product | None:
        if role!="admin":
            return None

        db_pro = await db.get(Product, pro_id)
        if db_pro:
            await db.delete(db_pro)
            await db.flush()

            return db_pro
            
        return None