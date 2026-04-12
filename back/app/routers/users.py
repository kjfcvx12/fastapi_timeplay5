from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import set_auth_cookies

from app.db.database import get_db

from app.db.scheme.users import UserRead, UserLogin, UserCreate, UserUpdate

from app.services.users import UserService



router=APIRouter(prefix='/users',tags=['User'])


# 회원가입
@router.post('/signup',response_model=UserRead)
async def signup(user:UserCreate, db:AsyncSession=Depends(get_db)):
    return await UserService.se_us_create(db, user)


# 로그인
@router.post("/login")
async def login(user:UserLogin, response:Response, db:AsyncSession=Depends(get_db)):
    result=await UserService.se_us_login(db, user)
    db_user, access_token, refresh_token=result
    set_auth_cookies(response, access_token, refresh_token)
    return {"message": "로그인 성공"}

# 로그아웃
@router.post("/logout")
async def logout(response:Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"로그아웃성공"}


# GET		/users/id/{user_id}	특정 id 사용자 조회
@router.get('/{user_id}', response_model=UserRead)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.se_us_get_id(db, user_id)


# PUT		/users/edit/{user_id}	특정 id 사용자 수정
@router.put("/edit", response_model=UserRead)
async def update_user_id(user_update: UserUpdate, 
                         user_id: int = Depends(get_user_id),  
                         db: AsyncSession = Depends(get_db)):
    return await UserService.se_us_update(db, user_id, user_update)


# DELETE		/users/del/{user_id}	특정 id 사용자 삭제
@router.delete("/del", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_id(user_id:int=Depends(get_user_id),
                         db: AsyncSession = Depends(get_db)):
    await UserService.se_us_delete(db,user_id)