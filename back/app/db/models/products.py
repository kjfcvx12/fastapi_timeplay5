from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import List, TYPE_CHECKING 


if TYPE_CHECKING:
    from .procarts import ProCart
    from .orderdetails import OrderDetail
    from .reviews import Review

class Product(Base):
    __tablename__="products"

    pro_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pro_name: Mapped[str] =mapped_column(String(100), nullable=False)
    qty: Mapped[int] =mapped_column(nullable=False, default=0)
    price: Mapped[int] =mapped_column(nullable=False, default=0)
    
    carts: Mapped[List["ProCart"]] = relationship(back_populates="product")
    orderdetails: Mapped[List["OrderDetail"]] = relationship(back_populates="product")
    reviews: Mapped[List["Review"]] = relationship(back_populates="product")
    
    
