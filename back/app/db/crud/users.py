from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.db.models.users import User 
from app.db.scheme.users import UserCreate, UserUpdate, UserLogin
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime,timedelta,timezone


class UserCrud:
    @staticmethod
    async def cr_us_get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    
    @staticmethod
    async def cr_us_create(db:AsyncSession, user: UserCreate,hashed_pw:str) -> User:
              
        user_data = user.model_dump()
        user_data["pw"] = hashed_pw
        db_user=User(**user_data)
        db.add(db_user)
        await db.flush()
        return db_user

    @staticmethod
    async def cr_us_update(db:AsyncSession,user_id:int,user_data:dict)->User|None:
        db_user=await db.get(User, user_id)
        
        if db_user:           
            for key,value in user_data.items():
                setattr(db_user,key,value)
            await db.flush()
            return db_user
            
        return None
    
    @staticmethod
    async def cr_us_get_id(db:AsyncSession,user_id:int) -> User | None:
        db_user = await db.get(User,user_id)
        return db_user

    @staticmethod
    async def cr_us_update_token(db: AsyncSession, user_id: int, token: str | None) -> bool:
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.refresh_token = token
            await db.flush()
            return True
        return False

    @staticmethod
    async def cr_us_delete(db:AsyncSession , user_id:int)->User|None:
        db_user = await db.get(User,user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None
 
