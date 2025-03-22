from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, slides
from app.infrastructure.database.database import Base, engine
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = FastAPI(
    title="Slide Management API",
    description="API for managing HTML and SVG slides",
    version="0.1.0",
)

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # ←データ消える！
        await conn.run_sync(Base.metadata.create_all)

# CORSの許可オリジンを設定
allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Slide Management API"}

# APIルーターの登録
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(slides.router, prefix="/api", tags=["slides"])