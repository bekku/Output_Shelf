from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.slide import Slide, SlideId
from app.domain.entities.user import UserId


class SlideRepository(ABC):
    """スライドリポジトリのインターフェース"""

    @abstractmethod
    async def save(self, slide: Slide) -> Slide:
        """スライドを保存する"""
        pass

    @abstractmethod
    async def find_by_id(self, slide_id: SlideId) -> Optional[Slide]:
        """IDによりスライドを検索する"""
        pass

    @abstractmethod
    async def find_by_owner(self, owner_id: UserId) -> List[Slide]:
        """所有者によりスライドを検索する"""
        pass

    @abstractmethod
    async def find_public(self) -> List[Slide]:
        """公開スライドを検索する"""
        pass

    @abstractmethod
    async def delete(self, slide_id: SlideId) -> bool:
        """スライドを削除する"""
        pass