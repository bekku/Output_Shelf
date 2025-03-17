from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SlideId(BaseModel):
    """スライドIDの値オブジェクト"""
    value: int


class Slide:
    """スライドのエンティティ"""

    def __init__(
        self,
        id: Optional[SlideId] = None,
        title: str = "",
        content: str = "",
        is_public: bool = True,
        owner_email: str = "",
        owner_username: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = id
        self._title = title
        self._content = content
        self._is_public = is_public
        self._owner_email = owner_email
        self._owner_username = owner_username
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()

    @property
    def id(self) -> Optional[SlideId]:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def is_public(self) -> bool:
        return self._is_public

    @property
    def owner_email(self) -> str:
        return self._owner_email

    @property
    def owner_username(self) -> str:
        return self._owner_username

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update(self, title: str, content: str, is_public: bool) -> None:
        """スライドの内容を更新する"""
        self._title = title
        self._content = content
        self._is_public = is_public
        self._updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "id": self._id.value if self._id else None,
            "title": self._title,
            "content": self._content,
            "is_public": self._is_public,
            "owner_email": self._owner_email,
            "owner_username": self._owner_username,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Slide":
        """辞書からインスタンスを生成"""
        id_value = data.get("id")
        id_obj = SlideId(value=id_value) if id_value is not None else None

        return cls(
            id=id_obj,
            title=data.get("title", ""),
            content=data.get("content", ""),
            is_public=data.get("is_public", True),
            owner_email=data.get("owner_email", ""),
            owner_username=data.get("owner_username", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )