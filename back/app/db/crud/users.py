from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.db.models.users import User 
from app.db.scheme.users import UserCreate, UserUpdate, UserLogin
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime,timedelta,timezone
import jwt


SECRET_KEY = '1234'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#jwt_handle 으로 분리

class UserAuth:
    @staticmethod
    def cr_us_get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def cr_us_verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def cr_us_create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# UserAuth는 jwt_handle 쪽으로 분리

class UserCrud:
    @staticmethod
    async def cr_us_login(db: AsyncSession, login_data: UserLogin) -> Optional[dict]:
        result = await db.execute(select(User).filter(User.email == login_data.email))
        user = result.scalars().first()
        if not user or not UserAuth.cr_us_verify_password(login_data.pw, user.pw):
            return None
        
        token_data = {"sub": user.email, "user_id": user.user_id, "role": user.role}
        access_token = UserAuth.cr_us_create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

    # 로그인 services 쪽 이동

    @staticmethod
    async def cr_us_create(db:AsyncSession, user: UserCreate) -> User:
        hashed_pw = UserAuth.cr_us_get_password_hash(user.pw)
        
        user_data = user.model_dump()
        user_data["pw"] = hashed_pw
        # 비밀번호 암호화 service 쪽 이동
        db_user=User(**user_data)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        # commit & refresh 제거 후 flush 교체
        return db_user

    @staticmethod
    async def cr_us_update(db:AsyncSession,user_id:int,user:UserUpdate)->User|None:
        db_user=await db.get(User, user_id)
        
        if db_user:
            update_data=user.model_dump(exclude_unset=True)
            for key,value in update_data.items():
                if key == "pw":
                    value = UserAuth.cr_us_get_password_hash(value)
                # key 조건은 service 쪽으로
                setattr(db_user,key,value)
            await db.flush()
            await db.commit()
            await db.refresh(db_user)
            # commit&refresh 제거
            return db_user
            
        return None
    
    @staticmethod
    async def cr_us_get_id(db:AsyncSession,user_id:int) -> User | None:
        db_user = await db.get(User,user_id)
        return db_user

    @staticmethod
    async def cr_us_logout(db: AsyncSession, user_id: int) -> bool:
        db_user=await db.get(User,user_id)
        if db_user:
            db_user.refresh_token=None
            await db.flush()
            await db.commit()
            return True
        
        return False
    
    # services 쪽 이동

    @staticmethod
    async def cr_us_delete(db:AsyncSession , user_id:int)->User|None:
        db_user = await db.get(User,user_id)
        if db_user:
            await db.delete(db_user)
            await db.commit()
            # commit 말고 flush
            return db_user
        return None
 
