from typing import List, Optional

from app.application.interfaces.slide_dto import (
    SlideCreateDTO,
    SlideResponseDTO,
    SlideUpdateDTO
)
from app.domain.entities.slide import Slide, SlideId
from app.domain.entities.user import UserId
from app.domain.repositories.slide_repository import SlideRepository


class SlideUseCases:
    """スライドのユースケース"""

    def __init__(self, slide_repository: SlideRepository):
        self.slide_repository = slide_repository

    async def create_slide(
        self, slide_data: SlideCreateDTO, current_user
    ) -> SlideResponseDTO:
        """
        スライドを作成する

        Args:
            slide_data: 作成するスライドのデータ
            current_user: 現在のユーザー（UserResponseDTO）

        Returns:
            作成されたスライドのDTO
        """
        # スライドエンティティを作成
        slide = Slide(
            title=slide_data.title,
            content=slide_data.content,
            is_public=slide_data.is_public,
            owner_email=current_user.email,
            owner_username=current_user.username
        )

        # リポジトリを使用してスライドを保存
        saved_slide = await self.slide_repository.save(slide)

        # DTOに変換して返す
        return self._to_dto(saved_slide)

    async def get_slides_by_user(self, user) -> List[SlideResponseDTO]:
        """
        ユーザーのスライドを取得する

        Args:
            user: スライドを取得するユーザー（UserResponseDTO）

        Returns:
            ユーザーのスライドDTOのリスト
        """
        # リポジトリを使用してユーザーのスライドを取得
        # DTOオブジェクトからemailを使用してUserIdを作成
        owner_id = UserId(value=user.email)
        slides = await self.slide_repository.find_by_owner(owner_id)

        # DTOのリストに変換して返す
        return [self._to_dto(slide) for slide in slides]

    async def get_public_slides(self) -> List[SlideResponseDTO]:
        """
        公開スライドを取得する

        Returns:
            公開スライドDTOのリスト
        """
        # リポジトリを使用して公開スライドを取得
        slides = await self.slide_repository.find_public()

        # DTOのリストに変換して返す
        return [self._to_dto(slide) for slide in slides]

    async def get_slide_by_id(
        self, slide_id: int, current_user=None
    ) -> Optional[SlideResponseDTO]:
        """
        IDによりスライドを取得する

        Args:
            slide_id: 取得するスライドのID
            current_user: 現在のユーザー（UserResponseDTOまたはNone）

        Returns:
            スライドDTO（存在しない場合またはアクセス権がない場合はNone）
        """
        # リポジトリを使用してスライドを取得
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))

        if not slide:
            return None

        # 非公開スライドは所有者のみアクセス可能
        if not slide.is_public and (
            not current_user or slide.owner_email != current_user.email
        ):
            return None

        # DTOに変換して返す
        return self._to_dto(slide)

    async def update_slide(
        self, slide_id: int, slide_data: SlideUpdateDTO, current_user
    ) -> Optional[SlideResponseDTO]:
        """
        スライドを更新する

        Args:
            slide_id: 更新するスライドのID
            slide_data: 更新データ
            current_user: 現在のユーザー（UserResponseDTO）

        Returns:
            更新されたスライドDTO（存在しない場合またはアクセス権がない場合はNone）
        """
        # リポジトリを使用してスライドを取得
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))

        if not slide:
            return None

        # 所有者のみ編集可能
        if slide.owner_email != current_user.email:
            return None

        # スライドを更新
        slide.update(
            title=slide_data.title,
            content=slide_data.content,
            is_public=slide_data.is_public
        )

        # 更新したスライドを保存
        updated_slide = await self.slide_repository.save(slide)

        # DTOに変換して返す
        return self._to_dto(updated_slide)

    async def delete_slide(
        self, slide_id: int, current_user
    ) -> bool:
        """
        スライドを削除する

        Args:
            slide_id: 削除するスライドのID
            current_user: 現在のユーザー（UserResponseDTO）

        Returns:
            削除が成功したかどうか
        """
        # リポジトリを使用してスライドを取得
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))

        if not slide:
            return False

        # 所有者のみ削除可能
        if slide.owner_email != current_user.email:
            return False

        # スライドを削除
        return await self.slide_repository.delete(SlideId(value=slide_id))

    def _to_dto(self, slide: Slide) -> SlideResponseDTO:
        """
        スライドエンティティをDTOに変換する

        Args:
            slide: 変換するスライドエンティティ

        Returns:
            スライドDTO
        """
        return SlideResponseDTO(
            id=slide.id.value,
            title=slide.title,
            content=slide.content,
            is_public=slide.is_public,
            owner_email=slide.owner_email,
            owner_username=slide.owner_username,
            created_at=slide.created_at,
            updated_at=slide.updated_at
        )