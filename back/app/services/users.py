from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.crud.users import UserCrud
from app.db.scheme.users import UserCreate, UserUpdate, UserLogin
from app.core.jwt_handle import get_password_hash, verify_password, create_access_token, create_refresh_token

class UserService:
    @staticmethod
    async def se_us_create(db:AsyncSession, user:UserCreate):
        hashed_pw = get_password_hash(user.pw)
        new_user = await UserCrud.cr_us_create(db, user, hashed_pw)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    # se_us_create
    # 동일한 이메일을 가진 유저가 있을 경우 접속을 막기위한 에러처리
    
    @staticmethod
    async def se_us_login(db: AsyncSession, login_data: UserLogin):
        user=await UserCrud.cr_us_get_by_email(db,login_data.email)
        
        if not user or not verify_password(login_data.pw, user.pw):
            raise HTTPException(
                status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")
        
        token_data = {"sub": user.email, "user_id": user.user_id, "role": user.role}
        access_token = create_access_token(uid=user.user_id,**token_data)
        refresh_token = create_refresh_token(uid=user.user_id)
        
        await UserCrud.cr_us_update_token(db, user.user_id, refresh_token)
        await db.commit()
        return {
            "access_token": access_token,
            "refresh_token":refresh_token,
            "token_type": "bearer",
            "user": user
        }
    
    @staticmethod
    async def se_us_update(db:AsyncSession,user_id:int, user_update:UserUpdate):
        update_data=user_update.model_dump(exclude_unset=True)

        
        if "pw" in update_data and update_data["pw"] is not None:
            update_data["pw"] = get_password_hash(update_data["pw"])
        update_user=await UserCrud.cr_us_update(db,user_id,update_data)
        if update_user:
            await db.commit()
            await db.refresh(update_user)

        return update_user
    
    # se_us_update
    # "if "pw" in update_data and update_data["pw"] is not None:
    # 수정 정보 중에 pw 데이터가 있는지 물어 보고 있으면 암호화
    # if update_data.get("pw"): 

    
    @staticmethod
    async def se_us_logout(db: AsyncSession, user_id: int) -> bool:
        logout=await UserCrud.cr_us_update_token(db,user_id,None)
        if logout:             
            await db.commit()
            return True
        
        return False
    
    # se_us_logout
    # 로그아웃 부분은 db를 건드릴 필요가 없음
    
    @staticmethod
    async def se_us_get_id(db: AsyncSession, user_id: int):
        return await UserCrud.cr_us_get_id(db, user_id)
    
    @staticmethod
    async def se_us_delete(db: AsyncSession, user_id: int) -> bool:
        
        delete_user = await UserCrud.cr_us_delete(db, user_id)
        
        if delete_user:
            await db.commit()
            return True
        return False
    

    # se_us_delete
    # 유저 삭제 실패 예외처리
    # 삭제 실패시 rollback