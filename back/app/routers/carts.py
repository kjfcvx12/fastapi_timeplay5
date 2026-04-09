from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.carts import CaRead
from app.db.scheme.procarts import PrCartCreate, PrCartUpdate, PrCartRead

from app.core.auth import get_user_id

from app.services.carts import CartService


router=APIRouter(prefix="/cart", tags=["cart"])



# 장바구니 전체 검색
@router.get("/all", response_model=list[PrCartRead])
async def ro_cart_get_all(user_id:int=Depends(get_user_id), 
                            db:AsyncSession=Depends(get_db)):
    return await CartService.se_cart_get_all(db, user_id)

# 장바구니 상품 id 검색
@router.get("/id/{pro_id}", response_model=PrCartRead)
async def ro_prcart_get_id(pro_id:int, user_id:int=Depends(get_user_id), 
                           db:AsyncSession=Depends(get_db)):

    return await CartService.se_prcart_get_pro_id(db, user_id, pro_id)

# 장바구니 상품 이름 검색
@router.get("/name/{pro_name}", response_model=PrCartRead)
async def ro_prcart_get_name(pro_name:str, user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await CartService.se_cart_get_name(db, user_id, pro_name)

# 장바구니 상품 추가
@router.post("", response_model=PrCartRead, status_code=status.HTTP_201_CREATED)
async def ro_prcart_create(prcart:PrCartCreate,
                       user_id:int=Depends(get_user_id),
                       db:AsyncSession=Depends(get_db)):
    return await CartService.se_add_or_update(db, user_id, prcart)

# 장바구니 상품 수정
@router.put("/{pro_cart_id}", response_model=PrCartRead, status_code=status.HTTP_200_OK)
async def ro_prcart_update(prcart:PrCartUpdate,
                           pro_cart_id: int,
                           user_id:int=Depends(get_user_id),
                           db:AsyncSession=Depends(get_db)):
    return await CartService.se_prcart_update(db, prcart, pro_cart_id)

# 장바구니 상품 삭제
@router.delete("/{pro_cart_id}", response_model=PrCartRead, status_code=status.HTTP_200_OK)
async def ro_prcart_delete(pro_cart_id:int,
                       user_id:int=Depends(get_user_id),
                       db:AsyncSession=Depends(get_db)):
    return await CartService.se_prcart_delete(db, pro_cart_id)


# 장바구니 상품 전체 삭제
@router.delete("/delete", response_model=PrCartRead, status_code=status.HTTP_200_OK)
async def ro_ca_delete(db:AsyncSession=Depends(get_db), user_id:int=Depends(get_user_id)):
    return await CartService.se_ca_delete(db, user_id)
