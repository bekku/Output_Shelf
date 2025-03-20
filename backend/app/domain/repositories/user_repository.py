from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User


class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース"""

    @abstractmethod
    async def save(self, user: User) -> User:
        """
        ユーザーを保存する

        既存ユーザーの場合は更新、存在しない場合は新規作成

        Args:
            user: 保存するユーザーエンティティ

        Returns:
            保存されたユーザーエンティティ
        """
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """
        IDによりユーザーを検索する

        Args:
            user_id: 検索するユーザーID

        Returns:
            ユーザーエンティティ（存在しない場合はNone）
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        メールアドレスによりユーザーを検索する

        Args:
            email: 検索するメールアドレス

        Returns:
            ユーザーエンティティ（存在しない場合はNone）
        """
        pass