from fastapi import Request

from app.core.jwt_handle import verify_token, create_access_token, create_refresh_token
from app.core.auth import set_auth_cookies
from app.db.crud.users import UserCrud
from app.db.database import get_db

from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError


# 클라이언트가 호출하면 미들웨어가 먼저 실행된다
# 액세스토큰을 먼저 확인 -> 리프레시 토큰 확인
# 미들웨어 없으면, 15분 마다 토큰만료에러 보고 다시 로그인을 해야됨...
# => 자동으로 새로운 액세스토큰 발급받고 요청 계속 진행시키기 위해 미들웨어에다 넣음

# BaseHTTPMiddleware를 상속받아 미들웨어를 만들거임
# 요청(request) -> 처리 (handler) -> 응답(response) 사이에 추가로직 삽입 가능
# call_next(request) : 다음 미들웨어 or 라우터 요청이 전달된다
class RefreshTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        response = await call_next(request)

        #쿠키에서 토큰 가져옴
        access_token=request.cookies.get("access_token")
        refresh_token=request.cookies.get("refresh_token")
        #액세스토큰 존재하면, 유효성 검증 => 만료/잘못된 토큰이면 pass -> 리프레시로 이동
        try:
            if access_token:
                verify_token(access_token)
                return response
            
        except (ExpiredSignatureError, InvalidTokenError):
            pass

        #리프레시 토큰 존재하면 검증시도, 정상이면 user_id 가져옴
        #만료/잘못된 토큰이면 기존 응답 반환
        if refresh_token:
            try:
                user_id=verify_token(refresh_token)
            
            except (ExpiredSignatureError, InvalidTokenError):
                return response

        
            new_access_token=create_access_token(user_id)
            new_refresh_token=create_refresh_token(user_id)

            #db에 새 리프레시 토큰 저장
            #anext() : 비동기 제네레이터에서 값 가져오는 함수 => 다음 세션객체 가져오려고
            try:
                db=await anext(get_db())
                await UserCrud.update_refresh_token_by_id(db, user_id, new_refresh_token)
                await db.commit()
            except Exception:
                await db.rollback()
                raise

            set_auth_cookies(response, new_access_token, new_refresh_token)
        
        return response