from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.db.scheme.orders import OrRead
from app.db.scheme.orders import OrCreate, OrRead, OrUpdate

from app.db.models.orders import Order
from app.db.models.orderdetails import OrderDetail 

from typing import Optional


class OrService:
# 주문 조회 전체 order

# 주문 조회 유저 주문 전체 od

# 주문 조회 주문 id od

# 주문 조회 날짜 od

# 주문 생성 order


# 주문 수정 상태 수정 관리자 order

# 주문 삭제 order

# 주문 생성 삭제시 개수 변화 od



    @staticmethod
    async def cr_or_update_pro(db: AsyncSession, pro_id: int, pro_qty: int):
        result = await db.execute(select(Product).filter(Product.pro_id == pro_id))
        product = result.scalar_one_or_none()
        if product and product.qty >= pro_qty:
            product.qty -= pro_qty
            await db.refresh(result, ['product'])
            return True
        return False


    



    @staticmethod
    async def se_cart_get_cart_id(db:AsyncSession, user_id:int) -> Optional[int]:
        db_cart=await PrCartCrud.cr_ca_get_id(db,user_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니가 없습니다.")
        return db_cart

    @staticmethod
    async def se_cart_get_all(db:AsyncSession, user_id:int) -> list[ProCart]:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)
        
        db_procart=await PrCartCrud.cr_prcart_get_all(db, cart_id)

        if not db_procart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 담긴 상품이 없습니다.")
        return db_procart
    
    @staticmethod
    async def se_prcart_get_pro_id(db:AsyncSession, user_id:int, pro_id:int)->ProCart:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)

        db_cart=await PrCartCrud.cr_prcart_get_id(db, pro_id, cart_id)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 찾으시는 id의 상품은 없습니다.")
        return db_cart
    
    @staticmethod
    async def se_cart_get_name(db:AsyncSession, user_id:int, pro_name:str)->list[ProCart]:
        cart_id=await CartService.se_cart_get_cart_id(db, user_id)

        db_cart=await PrCartCrud.cr_prcart_get_name(db, cart_id, pro_name)

        if not db_cart:
            raise HTTPException(status_code=404, 
                                detail="장바구니에 찾으시는 이름의 상품은 없습니다.")
        return db_cart


# cart 상품 추가시 상품이 존재하면 수정, 아니면 추가
    @staticmethod
    async def se_add_or_update(db: AsyncSession, user_id: int, 
                               prcart:PrCartCreate) -> ProCart:
        try:
            cart_id=await CartService.se_cart_get_cart_id(db, user_id)

            pro = await PrCartCrud.cr_prcart_get_pro_id(db, prcart.pro_id, cart_id)

            if pro:
                new_qty = pro.qty + prcart.qty
                result=await PrCartCrud.cr_prcart_update_qty(db, pro.pro_cart_id, new_qty)
                await db.commit()
                await db.refresh(result)
                return result
            else:
                result=await PrCartCrud.cr_prcart_create(db, prcart)
            
            await db.commit()
            await db.refresh(result)

            return result
        
        except HTTPException:
            await db.rollback()
            raise
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 등록 실패: {str(e)}")


# 장바구니 상품 수정 
    @staticmethod
    async def se_prcart_update(db:AsyncSession, prcart:PrCartUpdate, pro_cart_id:int) -> ProCart | None:
        try:
        
            db_prcart=await PrCartCrud.cr_prcart_update_by_id(db, prcart, pro_cart_id)

            if not db_prcart:
                raise HTTPException(status_code=404, 
                                detail="장바구니에 찾으시는 이름의 상품은 없습니다.")
            
            await db.commit()
            await db.refresh(db_prcart)
            
            return db_prcart
        
        except HTTPException:
            await db.rollback()
            raise


        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 수정 실패: {str(e)}")


# 장바구니 상품 삭제
    @staticmethod
    async def se_prcart_delete(db:AsyncSession, pro_cart_id:int) -> bool:     
        try:
            db_prcart=await PrCartCrud.cr_prcart_delete_by_id(db, pro_cart_id)

            if not db_prcart:
                raise HTTPException(status_code=404, 
                                detail="찾으시는 이름의 상품은 없습니다.")
            
            await db.commit()
            
            return True
        
        except HTTPException:
            await db.rollback()
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 삭제 실패: {str(e)}")


# 장바구니 상품 전부 지우기
    @staticmethod
    async def se_prcart_delete_all(db:AsyncSession, user_id:int)->int:
        try:
            cart_id=await CartService.se_cart_get_cart_id(db, user_id)
            
            db_cart=await PrCartCrud.cr_prcart_delete_all(db, cart_id)
            
            if not db_cart:
                raise HTTPException(status_code=404, 
                                    detail="장바구니에 상품이 없습니다.")
            
            await db.commit()

            return db_cart
        
        except HTTPException:
            await db.rollback()
            raise
    
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, 
                                detail=f"상품 삭제 실패: {str(e)}")



    
