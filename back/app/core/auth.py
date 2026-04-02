from fastapi import Request, Response, HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Optional

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
            raise HTTPException(status_code=401,detail="no uid")
        return user_id

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Acccess_token expired")
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Acccess_token")


#토크이 없거나 유효하지 않아도 오류 안던지고 그냥 None 반환함
async def get_optional(request:Request)-> Optional[int]:
    access_token=request.cookies.get("access_token")
    if not access_token:
        return None
    
    try:
        return verify_token(access_token)
    
    except (ExpiredSignatureError, InvalidTokenError):
        return None