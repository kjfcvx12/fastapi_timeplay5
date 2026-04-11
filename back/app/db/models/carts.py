from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey 

from typing import List, TYPE_CHECKING 

if TYPE_CHECKING:
    from .users import User
    from .procarts import ProCart

class Cart(Base):
    __tablename__="carts"

    cart_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    user_id: Mapped[int]= mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    
    
    user: Mapped["User"] = relationship(back_populates="cart")
    products: Mapped[List["ProCart"]] = relationship(back_populates="cart")
    
    
