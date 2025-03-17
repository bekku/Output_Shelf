from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User, UserId


class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース"""

    @abstractmethod
    async def save(self, user: User) -> User:
        """ユーザーを保存する"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """IDによりユーザーを検索する"""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """メールアドレスによりユーザーを検索する"""
        pass