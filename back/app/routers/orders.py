from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.orders import OrRead
from app.db.scheme.orders import OrCreate, OrRead, OrUpdate

from app.db.scheme.orderdetails import OrDeRead, OrDeCreate


from app.core.auth import get_user_id, get_admin_id

from app.services.orders import OrService


router=APIRouter(prefix="/order", tags=["order"])






# 주문 조회 전체 order
@router.get("/all", response_model=list[OrDeRead])
async def ro_or_get_all(user_id:int=Depends(get_user_id),
                            db:AsyncSession=Depends(get_db)):
    return await OrService.se_or_get_all(db, user_id)


# 주문 조회 유저 주문 전체 od

# 주문 조회 주문 id od

# 주문 조회 날짜 order,od

# 주문 생성 order

# 주문 수정 상태 수정 order

# 주문 삭제 od



# 장바구니 상품 id 검색
@router.get("/id/{pro_id}", response_model=PrCartRead)
async def ro_prcart_get_id(pro_id:int, 
                           user_id:int=Depends(get_user_id),
                           db:AsyncSession=Depends(get_db)):

    return await CartService.se_prcart_get_pro_id(db, user_id, pro_id)

# 장바구니 상품 이름 검색
@router.get("/name/{pro_name}", response_model=list[PrCartRead])
async def ro_prcart_get_name(pro_name:str, 
                             user_id:int=Depends(get_user_id),
                             db:AsyncSession=Depends(get_db)):
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
@router.delete("/{pro_cart_id}", status_code=status.HTTP_200_OK)
async def ro_prcart_delete(pro_cart_id:int,
                           user_id:int=Depends(get_user_id),
                           db:AsyncSession=Depends(get_db)):
    await CartService.se_prcart_delete(db, pro_cart_id)
    return {"detail": "상품이 삭제되었습니다."}

# 장바구니 상품 전체 삭제
@router.delete("/", status_code=status.HTTP_200_OK)
async def ro_prcart_delete_all(user_id:int=Depends(get_user_id),
                       db:AsyncSession=Depends(get_db)):
    await CartService.se_prcart_delete_all(db, user_id)
    return {"detail": "장바구니의 모든 상품이 삭제되었습니다."}