# 전체 주문내역

# 특정 날짜 주문내역 ordered_at

# 주문 상태 수정 관리자

# 주문 생성 유저

# 주문 취소 유저

# 상세 주문 내역



    @staticmethod
    async def cr_or_update_pro(db: AsyncSession, pro_id: int, pro_qty: int):
        result = await db.execute(select(Product).filter(Product.pro_id == pro_id))
        product = result.scalar_one_or_none()
        if product and product.qty >= pro_qty:
            product.qty -= pro_qty
            await db.flush()
            return True
        return False