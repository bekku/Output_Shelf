from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.slide import Slide


class SlideRepository(ABC):
    """スライドリポジトリのインターフェース"""

    @abstractmethod
    async def save(self, slide: Slide) -> Slide:
        """
        スライドを保存する

        新規作成の場合はidがNoneのスライドを渡す
        更新の場合はidが設定されたスライドを渡す

        Args:
            slide: 保存するスライドエンティティ

        Returns:
            保存されたスライドエンティティ
        """
        pass

    @abstractmethod
    async def find_by_id(self, slide_id: int) -> Optional[Slide]:
        """
        IDによりスライドを検索する

        Args:
            slide_id: 検索するスライドID

        Returns:
            スライドエンティティ（存在しない場合はNone）
        """
        pass

    @abstractmethod
    async def find_by_owner(self, owner_id: str) -> List[Slide]:
        """
        所有者によりスライドを検索する

        Args:
            owner_id: 所有者のユーザーID

        Returns:
            スライドエンティティのリスト
        """
        pass

    @abstractmethod
    async def find_public(self, page: int = 1, per_page: int = 18) -> tuple[List[Slide], int]:
        """
        公開スライドを検索する（ページネーション付き）

        Args:
            page: ページ番号（1から開始）
            per_page: 1ページあたりの表示数

        Returns:
            tuple[List[Slide], int]: (スライドのリスト, 総ページ数)
        """
        pass

    @abstractmethod
    async def delete(self, slide_id: int) -> bool:
        """
        スライドを削除する

        Args:
            slide_id: 削除するスライドID

        Returns:
            削除が成功したかどうか
        """
        pass