from typing import Optional
from pydantic import BaseModel

class User:
    """ユーザーのエンティティ"""

    def __init__(
        self,
        email: str,
        username: str,
        hashed_password: Optional[str] = None,
        id: Optional[int] = None,
    ):
        self._id = id
        self._email = email
        self._username = username
        self._hashed_password = hashed_password

    @property
    def id(self) -> str:
        return self._id

    @property
    def email(self) -> str:
        """IDとしてのメールアドレスを取得"""
        return self._email

    @property
    def username(self) -> str:
        return self._username

    @property
    def hashed_password(self) -> Optional[str]:
        return self._hashed_password

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "id": self._id,
            "email": self._email,
            "username": self._username,
            "hashed_password": self._hashed_password
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """辞書からインスタンスを生成"""
        return cls(
            id=data.get("id"),
            email=data.get("email"),
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password")
        )