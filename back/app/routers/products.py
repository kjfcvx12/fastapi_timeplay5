from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.scheme.products import PrCreate, PrRead, PrUpdate
from app.db.database import get_db
from app.services.products import ProService
from app.core.auth import get_admin_id


router=APIRouter(prefix="/product", tags=["Product"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)

# 상품 전체 검색
@router.get("/all", response_model=list[PrRead])
async def ro_pr_get_all(db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_get_all(db)

# 상품 id 검색
@router.get("/id/{pro_id}", response_model=PrRead)
async def ro_pr_get_id(pro_id:int, db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_get_id(db, pro_id)

# 상품 이름 검색
@router.get("/name/{pro_name}", response_model=list[PrRead])
async def ro_pr_get_name(pro_name:str, db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_get_name(db, pro_name)

# 상품 등록
@router.post("", response_model=PrRead, status_code=status.HTTP_201_CREATED)
async def ro_pr_create(product:PrCreate,
                       admin_id:int=Depends(get_admin_id),
                       token: str = Depends(oauth2_scheme),
                       db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_create(db, product)

# 상품 수정
@router.put("/{pro_id}", response_model=PrRead, status_code=status.HTTP_200_OK)
async def ro_pr_update(product:PrUpdate,
                       pro_id:int,
                       admin_id:int=Depends(get_admin_id),
                       token: str = Depends(oauth2_scheme),
                       db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_update(db, product, pro_id)

# 상품 삭제
@router.delete("/{pro_id}", response_model=PrRead, status_code=status.HTTP_200_OK)
async def ro_pr_delete(pro_id:int,
                       admin_id:int=Depends(get_admin_id),
                       token: str = Depends(oauth2_scheme),
                       db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_delete(db, pro_id)
