from datetime import timedelta
from typing import Optional

from app.application.interfaces.user_dto import (
    TokenDTO,
    UserCreateDTO,
    UserResponseDTO
)
from app.domain.entities.user import User, UserId
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.auth_service import AuthService


class AuthUseCases:
    """認証のユースケース"""

    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthService
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def register_user(
        self, user_data: UserCreateDTO
    ) -> Optional[UserResponseDTO]:
        """
        ユーザーを登録する

        Args:
            user_data: 登録するユーザーのデータ

        Returns:
            登録されたユーザーのDTO（既に存在する場合はNone）
        """
        # メールアドレスが既に登録されているか確認
        existing_user = await self.user_repository.find_by_email(
            user_data.email
        )
        if existing_user:
            return None

        # パスワードをハッシュ化
        hashed_password = self.auth_service.get_password_hash(
            user_data.password
        )

        # ユーザーエンティティを作成
        user = User(
            id=UserId(value=user_data.email),
            username=user_data.username,
            hashed_password=hashed_password
        )

        # リポジトリを使用してユーザーを保存
        saved_user = await self.user_repository.save(user)

        # DTOに変換して返す
        return self._to_dto(saved_user)

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[TokenDTO]:
        """
        ユーザーを認証する

        Args:
            email: ユーザーのメールアドレス
            password: ユーザーのパスワード

        Returns:
            認証トークンDTO（認証失敗時はNone）
        """
        # リポジトリを使用してユーザーを取得
        user = await self.user_repository.find_by_email(email)

        # 認証サービスを使用してユーザーを認証
        if not self.auth_service.authenticate_user(user, password):
            return None

        # アクセストークンを生成
        access_token_expires = timedelta(
            minutes=self.auth_service.access_token_expire_minutes
        )
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        return TokenDTO(
            access_token=access_token,
            token_type="bearer"
        )

    async def get_current_user(
        self, email: str
    ) -> Optional[UserResponseDTO]:
        """
        現在のユーザーを取得する

        Args:
            email: ユーザーのメールアドレス

        Returns:
            ユーザーDTO（存在しない場合はNone）
        """
        # リポジトリを使用してユーザーを取得
        user = await self.user_repository.find_by_email(email)

        if not user:
            return None

        # DTOに変換して返す
        return self._to_dto(user)

    def _to_dto(self, user: User) -> UserResponseDTO:
        """
        ユーザーエンティティをDTOに変換する

        Args:
            user: 変換するユーザーエンティティ

        Returns:
            ユーザーDTO
        """
        return UserResponseDTO(
            email=user.email,
            username=user.username
        )