from typing import Optional
from pydantic import BaseModel


class UserId(BaseModel):
    """ユーザーIDの値オブジェクト"""
    value: str  # メールアドレスをIDとして使用


class User:
    """ユーザーのエンティティ"""

    def __init__(
        self,
        id: UserId,
        username: str,
        hashed_password: Optional[str] = None
    ):
        self._id = id
        self._username = username
        self._hashed_password = hashed_password

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def email(self) -> str:
        """IDとしてのメールアドレスを取得"""
        return self._id.value

    @property
    def username(self) -> str:
        return self._username

    @property
    def hashed_password(self) -> Optional[str]:
        return self._hashed_password

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "email": self._id.value,
            "username": self._username,
            "hashed_password": self._hashed_password
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """辞書からインスタンスを生成"""
        return cls(
            id=UserId(value=data.get("email", "")),
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password")
        )