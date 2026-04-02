from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .order import Order
    from .product import Product

class OrderDetail(Base):
    __tablename__="orderdetails"

    od_id: Mapped[int] = mapped_column(primary_key=True)
    qty: Mapped[int] =mapped_column(nullable=False, default=0)
    price: Mapped[int] =mapped_column(nullable=False, default=0)
    
    pro_id: Mapped[int]= mapped_column(ForeignKey("products.pro_id"), nullable=False)
    order_id: Mapped[int]= mapped_column(ForeignKey("orders.order_id"), nullable=False)
    
    order: Mapped["Order"] = relationship(back_populates="orderdetails")
    product: Mapped["Product"] = relationship(back_populates="orderdetails")
    
    