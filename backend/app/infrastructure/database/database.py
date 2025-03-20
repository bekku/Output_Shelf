from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 非同期のPostgreSQLデータベース接続
# 環境変数から接続情報を取得
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/slidedb"
)
engine = create_async_engine(DATABASE_URL, echo=False)
# 非同期セッションを作成
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# model作成用の基底クラス
Base = declarative_base()


# FastAPIの依存性注入で使用するセッション取得関数
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    リクエスト処理中に非同期データベースセッションを提供し、処理終了後に自動的にクローズする
    FastAPIの依存性注入で使用する
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()