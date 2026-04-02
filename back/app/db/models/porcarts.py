from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey 

from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .product import Product
    from .cart import Cart

class ProCart(Base):
    __tablename__="procarts"

    pro_cart_id: Mapped[int] = mapped_column(primary_key=True)
    qty: Mapped[int] = mapped_column(nullable=False, default=1)
    
    pro_id: Mapped[int]= mapped_column(ForeignKey("products.pro_id"), nullable=False)
    cart_id: Mapped[int]= mapped_column(ForeignKey("carts.cart_id"), nullable=False)
    
    product: Mapped["Product"] = relationship(back_populates="carts")
    cart: Mapped["Cart"] = relationship(back_populates="products")
    
    
