from typing import List, Optional, Tuple
from datetime import datetime

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
            owner_username=current_user.username,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # リポジトリを使用してスライドを保存
        saved_slide = await self.slide_repository.save(slide)

        # DTOに変換して返す
        return self._to_dto(saved_slide)

    async def get_slide(self, slide_id: str) -> Optional[SlideResponseDTO]:
        """スライドを取得する"""
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))
        return self._to_dto(slide) if slide else None

    async def get_user_slides(
        self, owner_email: str, page: int = 1, per_page: int = 18
    ) -> Tuple[List[SlideResponseDTO], int]:
        """ユーザーのスライドを取得する（ページネーション付き）"""
        owner_id = UserId(value=owner_email)
        slides = await self.slide_repository.find_by_owner(owner_id)

        # ページネーション処理
        total_pages = (len(slides) + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_slides = slides[start_idx:end_idx]

        return [self._to_dto(slide) for slide in paginated_slides], total_pages

    async def get_public_slides(
        self, page: int = 1, per_page: int = 18
    ) -> Tuple[List[SlideResponseDTO], int]:
        """
        公開スライドを取得する（ページネーション付き）

        Returns:
            公開スライドDTOのリストと総ページ数
        """
        slides, total_pages = await self.slide_repository.find_public(
            page=page, per_page=per_page
        )
        return [self._to_dto(slide) for slide in slides], total_pages

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
        self, slide_id: str, slide_data: SlideUpdateDTO
    ) -> Optional[SlideResponseDTO]:
        """スライドを更新する"""
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))
        if not slide:
            return None

        slide.title = slide_data.title
        slide.content = slide_data.content
        slide.is_public = slide_data.is_public
        slide.updated_at = datetime.utcnow()

        updated_slide = await self.slide_repository.save(slide)
        return self._to_dto(updated_slide)

    async def delete_slide(self, slide_id: str) -> bool:
        """スライドを削除する"""
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