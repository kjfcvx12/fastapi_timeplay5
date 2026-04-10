import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager

from dotenv import load_dotenv

from app.db.database import Base, async_engine
from app.routers import products , reviews, users
from app.middleware.token_refresh import RefreshTokenMiddleware

load_dotenv(dotenv_path=".env")


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)

#app.add_middleware(RefreshTokenMiddleware)


app.include_router(users.router)
app.include_router(products.router)
# app.include_router(cart.router)
# app.include_router(order.router)
app.include_router(reviews.router)


if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)


#(C:\Users\hi\miniconda3\shell\condabin\conda-hook.ps1) ; (conda activate base)
#(C:\Users\hi\miniconda3\shell\condabin\conda-hook.ps1) ; (conda activate fastapi)
#uvicorn main:app --port=8081 --reload