from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.orders import OrRead
from app.db.scheme.orders import OrCreate, OrRead, OrUpdate, OrCreateRequest

from app.db.scheme.orderdetails import OrDeRead, OrDeCreate


from app.core.auth import get_user_id, get_admin_id

from app.services.orders import OrService

from datetime import datetime


router=APIRouter(prefix="/order", tags=["order"])


# 주문 조회 전체 order
@router.get("/all", response_model=list[OrRead])
async def ro_or_get_all(admin_id:int=Depends(get_admin_id),
                        db:AsyncSession=Depends(get_db)):
    return await OrService.se_order_get_all(db)


# 주문 조회 유저 주문 전체 order
@router.get("/user/{user_id}", response_model=list[OrRead])
async def ro_or_get_user_id(user_id:int,
                       admin_id:int=Depends(get_admin_id),
                       db:AsyncSession=Depends(get_db)):

    return await OrService.se_order_get_id(db, user_id)



# 주문 조회 날짜 order,od
@router.get("/date/{ordered_at}", response_model=list[OrRead])
async def ro_or_get_date(ordered_at:datetime,
                       admin_id:int=Depends(get_admin_id),
                       db:AsyncSession=Depends(get_db)):

    return await OrService.se_order_get_date(db, ordered_at)


# 주문 생성 order
@router.post("/create", response_model=OrRead)
async def ro_or_create(order_rq:OrCreateRequest,
                       user_id:int=Depends(get_user_id),
                       db:AsyncSession=Depends(get_db)):

    return await OrService.se_order_create(db, order_rq.order, order_rq.prcart)

# 주문 수정 상태 수정 order
@router.put("/update", response_model=OrRead)
async def ro_or_update(order:OrUpdate,
                       order_id:int,
                       admin_id:int=Depends(get_admin_id),
                       db:AsyncSession=Depends(get_db)):

    return await OrService.se_order_update(db, order, order_id)

# 주문 취소 od
@router.post("/cancel/{order_id}", response_model=OrRead)
async def ro_or_cancel(order_id:int,
                       user_id:int=Depends(get_user_id),
                       db:AsyncSession=Depends(get_db)):

    return await OrService.se_order_cancel(db, order_id)

# 주문 조회 주문 id od
@router.get("/detail/{order_id}", response_model=list[OrDeRead])
async def ro_or_get_order_id(order_id:int,
                       user_id:int=Depends(get_user_id),
                       db:AsyncSession=Depends(get_db)):

    return await OrService.se_order_get_od_id(db, order_id)