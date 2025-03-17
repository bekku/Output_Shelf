from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.user import User, UserId
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    """ユーザーリポジトリの実装"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        """ユーザーを保存する"""
        # 既存ユーザーを検索
        stmt = select(UserModel).where(UserModel.email == user.email)
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()

        if db_user:
            # 更新
            db_user.username = user.username
            if user.hashed_password:
                db_user.hashed_password = user.hashed_password
        else:
            # 新規作成
            db_user = UserModel(
                email=user.email,
                username=user.username,
                hashed_password=user.hashed_password
            )
            self.session.add(db_user)

        await self.session.flush()
        await self.session.refresh(db_user)

        # エンティティに変換して返す
        return User(
            id=UserId(value=db_user.email),
            username=db_user.username,
            hashed_password=db_user.hashed_password
        )

    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """IDによりユーザーを検索する"""
        return await self.find_by_email(user_id.value)

    async def find_by_email(self, email: str) -> Optional[User]:
        """メールアドレスによりユーザーを検索する"""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()

        if not db_user:
            return None

        # エンティティに変換して返す
        return User(
            id=UserId(value=db_user.email),
            username=db_user.username,
            hashed_password=db_user.hashed_password
        )