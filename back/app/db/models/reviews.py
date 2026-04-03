from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .users import User
    from .products import Product
    from .orderdetails import OrderDetail

class Review(Base):
    __tablename__="reviews"

    rev_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] =mapped_column(String(500), nullable=False)
    rating : Mapped[int] =mapped_column(nullable=False)
    
    pro_id: Mapped[int]= mapped_column(ForeignKey("products.pro_id"), nullable=False)
    user_id: Mapped[int]= mapped_column(ForeignKey("users.user_id"), nullable=False)
    od_id: Mapped[int]= mapped_column(ForeignKey("orderdetails.od_id"), nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="reviews")
    product: Mapped["Product"] = relationship(back_populates="reviews")
    orderdetail: Mapped["OrderDetail"] = relationship(back_populates="review")
    