from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.scheme.users import UserCreate, UserRead, UserLogin, UserUpdate
from app.services.users import UserService
from app.core.jwt_handle import verify_token
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router=APIRouter(prefix='/users',tags=['User'])

@router.post('/signup',response_model=UserRead)
async def signup(user:UserCreate, db:AsyncSession=Depends(get_db)):
    return await UserService.se_us_create(db, user)


@router.get('/{user_id}', response_model=UserRead)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    
    return await UserService.se_us_get_id(db, user_id)

# 에러 처리 services로 이동(완료)

@router.put("/{user_id}", response_model=UserRead)
async def update_user_id(user_update: UserUpdate, user_id: int = Depends(get_user_id),  db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    current_uid = verify_token(token)
    if current_uid != user_id:
        raise HTTPException(
            status_code=403, 
            detail="본인의 정보만 수정할 수 있습니다."
        )
    
    return await UserService.se_us_update(db, user_id, user_update)

# 에러 처리 services로 이동(완료)
# user_id:int=Depends(get_user_id) 로 현재 유저가 맞는지 확인 후 수정(완료)

@router.delete('/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_id(user_id:int=Depends(get_user_id), db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme),):
    
    now_user_id = verify_token(token)

    if now_user_id != user_id:
        raise HTTPException(status_code=403,detail="본인의 계정만 삭제할 수 있습니다.")

    await UserService.se_us_delete(db,user_id)

# 에러 처리 services로 이동(완료)
# user_id:int=Depends(get_user_id) 로 현재 유저가 맞는지 확인 후 삭제(완료)

    
@router.post("/login")
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):

    login_result = await UserService.se_us_login(db, user)

    response.set_cookie(
        key="access_token", 
        value=login_result["access_token"], 
        )
    response.set_cookie(
        key="refresh_token", 
        value=login_result["refresh_token"], 
        )
    return {"message": "로그인 성공"}

# 로그인 후 현재 유저, accesss_token, refresh_token 쿠키 저장(완료)

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"로그아웃성공"}


# 로그아웃 부분은 현재 컴퓨터의 사용자의 데이터만 지우면 되기때문에 쿠키만 삭제(완료)
# db 건드릴 필요 없음(완료)
