from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

#공통 속성
class ReviewBase(BaseModel):
    content : str
    rating : int = Field(ge=0, le=5)
    pro_id : int
    od_id : int

#리뷰 작성
class ReviewCreate(ReviewBase):
    pass

#리뷰 수정
class ReviewUpdate(BaseModel):
    content : str | None = None
    rating : Optional[int] = Field(ge=0, le=5)

#DB에 저장
class ReviewInDB(ReviewBase):
    user_id : int
    rev_id : int
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
        #ORM 객체(SQLAlchemy)를 그대로 Pydantic 모델로 변환

#리뷰 조회
class ReviewRead(ReviewInDB):
    pass