from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Slide:
    """スライドのエンティティ"""

    def __init__(
        self,
        id: id = None,
        title: str = "",
        content: str = "",
        is_public: bool = True,
        owner_id: int = 0,
        owner_username: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = id
        self._title = title
        self._content = content
        self._is_public = is_public
        self._owner_id = owner_id
        self._owner_username = owner_username
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        self._updated_at = datetime.utcnow()

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value
        self._updated_at = datetime.utcnow()

    @property
    def is_public(self) -> bool:
        return self._is_public

    @is_public.setter
    def is_public(self, value: bool) -> None:
        self._is_public = value
        self._updated_at = datetime.utcnow()

    @property
    def owner_id(self) -> int:
        return self._owner_id

    @property
    def owner_username(self) -> str:
        return self._owner_username

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        self._updated_at = value

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "id": self._id.value if self._id else None,
            "title": self._title,
            "content": self._content,
            "is_public": self._is_public,
            "owner_id": self._owner_id,
            "owner_username": self._owner_username,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Slide":
        """辞書からインスタンスを生成"""

        return cls(
            id=data.get("id", None),
            title=data.get("title", ""),
            content=data.get("content", ""),
            is_public=data.get("is_public", True),
            owner_id=data.get("owner_id", 0),
            owner_username=data.get("owner_username", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )