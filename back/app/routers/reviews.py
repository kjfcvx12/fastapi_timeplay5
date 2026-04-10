from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.reviews import ReviewCreate, ReviewRead, ReviewUpdate
from app.services.reviews import ReviewService
from app.core.auth import get_user_id
from app.db.crud.reviews import ReviewCrud
from typing import List

router = APIRouter(prefix="/reviews", tags=["Reviews"])

#리뷰 작성
@router.post("", response_model=ReviewRead)
async def ro_re_create(
    review_data:ReviewCreate,
    user_id:int=Depends(get_user_id),
    db:AsyncSession=Depends(get_db)):

    return await ReviewService.se_re_create(db, user_id, review_data)

#리뷰 수정
@router.post("/{rev_id}", response_model=ReviewRead)
async def ro_re_update(
    rev_id:int,
    review_data:ReviewUpdate,
    user_id:int=Depends(get_user_id),
    db:AsyncSession=Depends(get_db)):

    return await ReviewService.se_re_update(db, user_id, rev_id, review_data)

#리뷰 삭제
@router.delete("/{rev_id}")
async def ro_re_delete(
    rev_id:int,
    user_id:int=Depends(get_user_id),
    db:AsyncSession=Depends(get_db)):

    return await ReviewService.se_re_delete(db, user_id, rev_id)

#리뷰 조회

#rev_id
@router.get("/{rev_id}", response_model=ReviewRead)
async def ro_re_get_rev_id(rev_id:int, db:AsyncSession=Depends(get_db)):
    return await ReviewCrud.cr_re_get_rev_id(db, rev_id)

#pro_id 모든 리뷰
@router.get("/product/{pro_id}", response_model=List[ReviewRead])
async def ro_re_get_pro_id(pro_id:int, db:AsyncSession=Depends(get_db)):
    return await ReviewCrud.cr_re_get_pro_id(db, pro_id)

#user_id 모든 리뷰
@router.get("/me", response_model=List[ReviewRead])
async def ro_re_get_user_id(user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await ReviewCrud.cr_re_get_user_id(db, user_id)

#전체 리뷰
@router.get("", response_model=List[ReviewRead])
async def ro_re_get_all(db:AsyncSession=Depends(get_db)):
    return await ReviewCrud.cr_re_get_all(db)





