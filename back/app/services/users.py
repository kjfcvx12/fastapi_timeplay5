from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.db.crud.users import UserCrud
from app.db.crud.carts import CaCrud

from app.db.scheme.users import UserCreate, UserUpdate, UserLogin
from app.db.scheme.carts import CaCreate

from app.core.jwt_handle import get_password_hash, verify_password, create_access_token, create_refresh_token

class UserService:
    @staticmethod
    async def se_us_create(db:AsyncSession, user:UserCreate):

        try:
            already_user=await UserCrud.cr_us_get_by_email(db, user.email)

            if already_user:
                raise HTTPException(status_code=400, detail='이미 등록된 이메일 입니다.')
            
            hashed_pw = get_password_hash(user.pw)
            new_user = await UserCrud.cr_us_create(db, user, hashed_pw)
            
            cart_data=CaCreate(user_id=new_user.user_id)
            db_cart=await CaCrud.cr_ca_create(db, cart_data)
            await db.commit()
            await db.refresh(new_user)
            await db.refresh(db_cart)
            return new_user
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=404, detail=f"사용자 등록 실패 :{e}")
       
    
    @staticmethod
    async def se_us_login(db: AsyncSession, login_data: UserLogin):
        try:
            user=await UserCrud.cr_us_get_by_email(db,login_data.email)
            
            if not user or not verify_password(login_data.pw, user.pw):
                raise HTTPException(
                    status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")
            
            token_data = {"sub": user.email, "user_id": user.user_id, "role": user.role}
            access_token = create_access_token(uid=user.user_id,**token_data)
            refresh_token = create_refresh_token(uid=user.user_id)
            
            update_user=await UserCrud.cr_us_update_token(db, user.user_id, refresh_token)
            
            await db.commit()
            await db.refresh(update_user)
            return update_user, access_token, refresh_token
        
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=404, detail=f"로그인 실패 :{e}")
    
    @staticmethod
    async def se_us_update(db:AsyncSession,user_id:int, user_update:UserUpdate):
        update_data=user_update.model_dump(exclude_unset=True)
        
        if update_data.get("pw"): 
            update_data['pw']=get_password_hash(update_data["pw"])
        
        updated_model = UserUpdate(**update_data) 

        update_user=await UserCrud.cr_us_update(db,user_id,updated_model)
        
        if not update_user:
            raise HTTPException(status_code=404, detail="수정할 사용자가 없습니다")
        
        
        await db.commit()
        await db.refresh(update_user)

        return update_user
    
    
    @staticmethod
    async def se_us_get_id(db: AsyncSession, user_id: int):
        user = await UserCrud.cr_us_get_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404,detail='해당 id의 사용자가 없습니다')
        
        return user
    
    @staticmethod
    async def se_us_get_email(db: AsyncSession, email: str):
        user = await UserCrud.cr_us_get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404,detail='해당 email의 사용자가 없습니다')
        
        return user.email
    

    @staticmethod
    async def se_us_delete(db: AsyncSession, user_id: int) -> str:
        try: 
            delete_user = await UserCrud.cr_us_delete(db, user_id)
        
            if not delete_user:
                raise HTTPException(status_code=404, detail='삭제할 유저가 없습니다')

            await db.commit()
            return {'message : 유저 삭제'}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=404, detail=f"사용자 삭제 실패 :{e}")
    