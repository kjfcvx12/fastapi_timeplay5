from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.scheme.products import PrCreate, PrRead
from app.db.database import get_db
from app.services.products import ProService
from app.core.auth import get_user_id


router=APIRouter(prefix="/product", tags=["Product"])

@router.get("/", response_model=list[PrRead])
async def ro_pr_list_products(db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_get_all(db)

@router.post("/create", response_model=PrRead, status_code=status.HTTP_201_CREATED)
async def create_products(proudct:PrCreate, db:AsyncSession=Depends(get_db)):
    return await ProService.se_pr_create(db, proudct)
