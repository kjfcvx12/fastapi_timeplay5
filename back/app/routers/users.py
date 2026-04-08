from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.db.scheme.users import UserCreate, UserRead, UserLogin, UserUpdate
from app.services.users import UserService
from app.core.jwt_handle import UserAuth

router=APIRouter(prefix='/users',tags=['User'])

@router.post('/signup',response_model=UserRead)
async def signup(user:UserCreate, db:AsyncSession=Depends(get_db)):
    return await UserService.se_us_create(db, user)

@router.get('/{user_id}', response_model=UserRead)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.se_us_get_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404,detail='해당 id의 사용자가 없습니다')
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user_id(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user=await UserService.se_us_update(db,user_id,user_update)
    if not user:
        raise HTTPException(status_code=404, detail="수정할 사용자가 없습니다")
    return user

@router.delete('/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    success=await UserService.se_us_delete(db,user_id)
    if not success:
        raise HTTPException(status_code=404, detail="삭제할 사용자가 없습니다")
    
@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await UserService.se_us_login(db, user)
@router.post("/logout")
async def logout_user(token: str, db: AsyncSession = Depends(get_db)):
    user_id = UserAuth.verify_token(token)
    await UserService.se_us_logout(db, user_id)
    return {"로그아웃성공"}