from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, func

from datetime import datetime

from typing import Optional, List, TYPE_CHECKING 

if TYPE_CHECKING:
    from .cart import Cart
    from .order import Order
    from .review import Review


class User(Base):
    __tablename__="users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] =mapped_column(String(30), nullable=False)
    email: Mapped[str] =mapped_column(String(100), nullable=False, unique=True)
    pw: Mapped[str] =mapped_column(String(300), nullable=False)
    address:Mapped[str] =mapped_column(String(500), nullable=False)
    phone: Mapped[str] =mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime]= mapped_column(TIMESTAMP, server_default=func.now())
    role: Mapped[str] =mapped_column(String(30), default="user")
    refresh_token: Mapped[Optional[str]]=mapped_column(String(300), nullable=True)
    
    cart: Mapped["Cart"] = relationship(back_populates="user", cascade="all, delete-orphan", uselist=False)
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")
		
		
		