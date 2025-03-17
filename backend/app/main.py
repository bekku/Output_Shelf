from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, slides
from app.infrastructure.database.database import Base, engine

app = FastAPI(
    title="Slide Management API",
    description="API for managing HTML and SVG slides",
    version="0.1.0",
)

# 起動時にデータベーステーブルを作成
@app.on_event("startup")
async def init_db():
    # テストとデバッグ目的のみ - 本番環境ではAlembicを使用すべき
    async with engine.begin() as conn:
        # テーブルの作成（開発環境のみ）
        await conn.run_sync(Base.metadata.create_all)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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