from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .orders import Order
    from .products import Product
    from .reviews import Review

class OrderDetail(Base):
    __tablename__="orderdetails"

    od_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    qty: Mapped[int] =mapped_column(nullable=False, default=0)
    price: Mapped[int] =mapped_column(nullable=False, default=0)
    
    pro_id: Mapped[int]= mapped_column(ForeignKey("products.pro_id", ondelete="CASCADE"), nullable=False)
    order_id: Mapped[int]= mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    
    order: Mapped["Order"] = relationship(back_populates="orderdetails")
    product: Mapped["Product"] = relationship(back_populates="orderdetails")
    review: Mapped["Review"] = relationship(back_populates="orderdetail")
    