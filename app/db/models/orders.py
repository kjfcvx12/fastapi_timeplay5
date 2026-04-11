from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, func, ForeignKey

from datetime import datetime

from typing import Optional, List, TYPE_CHECKING 

if TYPE_CHECKING:
    from .users import User
    from .orderdetails import OrderDetail



class Order(Base):
    __tablename__="orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ordered_at: Mapped[Optional[datetime]]= mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)
    total: Mapped[int] =mapped_column(nullable=False)
    pay: Mapped[int] =mapped_column(nullable=False)
    order_state: Mapped[int] =mapped_column(nullable=False, default=0)
    
    user_id: Mapped[int]= mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="orders")
    orderdetails: Mapped[List["OrderDetail"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    
    
    
    