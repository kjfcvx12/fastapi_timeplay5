from fastapi import Request, Response, HTTPException, Depends, status
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models.users import User

from app.core.settings import settings
from app.core.jwt_handle import verify_token


#JWT토큰을 쿠키로 설정하려고
#httponly=True : 쿠키를 만들면 js에서 접근 불가(xss공격방어)
#samesite="Lax" 외부 도메인 요청 시 쿠키 전송 제한됨
def set_auth_cookies(response:Response, access_token:str, refresh_token:str)->None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=int(settings.access_token_expire.seconds),
        secure=False,
        httponly=True,
        samesite="Lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=int(settings.refresh_token_expire.seconds),
        secure=False,
        httponly=True,
        samesite="Lax"
    )


#사용자 쿠키에 액세스 토큰있는지 확인
#쿠키에서 가져온 액세스 토큰 검증/유효한지 안한지 -> 인증 로직
async def get_user_id(request:Request)-> int:
    access_token=request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access_token missing")
    
    #토큰에서 사용자 id를 추출함 -> 정상적인 토큰이면 사용자 id 반환
    try:
        user_id=verify_token(access_token)
        if user_id is None:
            raise HTTPException(status_code=401,detail="현재 사용자가 없습니다.")
        return user_id

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Acccess_token expired")
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Acccess_token")


async def get_admin_id(user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)) -> int:
  
    result = await db.execute(select(User.role).filter(User.user_id == user_id))
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="사용자가 없습니다.")
    
    if role!='admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="관리자 권한이 필요합니다.")
    
    return user_id

#토크이 없거나 유효하지 않아도 오류 안던지고 그냥 None 반환함
async def get_optional(request:Request)-> Optional[int]:
    access_token=request.cookies.get("access_token")
    if not access_token:
        return None
    
    try:
        return verify_token(access_token)
    
    except (ExpiredSignatureError, InvalidTokenError):
        return None