from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone
import jwt
import uuid

from app.core.settings import settings

#해싱방식과 정책관리 (bcrypt 알고리즘 사용)
pwd_crypt=CryptContext(schemes=["bcrypt"])

class UserAuth:
    @staticmethod
    def get_password_hash(password: str) -> str:
        trunc_password = password.encode('utf-8')[:72]
        return pwd_crypt.hash(trunc_password)
    
    @staticmethod
    def verify_password(plain_pw:str, hashed_pw:str)->bool:
        trunc_password=plain_pw.encode('utf-8')[:72]
        return pwd_crypt.verify(trunc_password,hashed_pw)

    #jwt 생성함수  
    #암호화된 jwt문자열 반환
    @staticmethod
    def create_token(uid:int, expires_delta_seconds: int, **kwargs) -> str:
        to_encode=kwargs.copy()
        expire=datetime.now(timezone.utc) + timedelta(seconds=expires_delta_seconds)
        to_encode.update({"exp":expire, "uid":uid})
        encoded_jwt=jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    #create_token함수 호출해서 jwt 생성->uid, exp 포함->kwargs 없으면 playload는 uid, exp만 있음
    @staticmethod
    def create_access_token(uid:int, **kwargs)->str:
        return UserAuth.create_token(uid=uid, expires_delta_seconds=settings.access_token_expire_seconds,**kwargs)

    #리프레시 토큰 관리(재발급/ 로그아웃 시 무효화)
    #jti(jwt id): 서버에서 토큰 재사용 방지 관리 기능
    #uuid : 전세계에서 유일하게 식별할 수 있는 128비트 값 생성
    @staticmethod
    def create_refresh_token(uid:int) -> str:
        return UserAuth.create_token(uid=uid, jti=str(uuid.uuid4()), expires_delta_seconds=settings.refresh_token_expire_seconds)


    #토근을 디코딩해서 payload를 딕셔너리로 반환
    #서명을 검증해서 토큰 변조 여부를 확인
    @staticmethod
    def decode_token(token:str)->dict:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )

    #토큰을 디코딩한 수 uid 값을 꺼낸다 -> 사용자 id
    @staticmethod
    def verify_token(token:str)->int:
        playload=UserAuth.decode_token(token)
        return playload.get("uid")
