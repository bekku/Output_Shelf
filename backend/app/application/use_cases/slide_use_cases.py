from typing import List, Optional

from app.application.interfaces.slide_dto import (
    SlideCreateDTO,
    SlideResponseDTO,
    SlideUpdateDTO
)
from app.domain.entities.slide import Slide, SlideId
from app.domain.entities.user import User
from app.domain.repositories.slide_repository import SlideRepository


class SlideUseCases:
    """スライドのユースケース"""

    def __init__(self, slide_repository: SlideRepository):
        self.slide_repository = slide_repository

    async def create_slide(
        self, slide_data: SlideCreateDTO, current_user: User
    ) -> SlideResponseDTO:
        """スライドを作成する"""
        slide = Slide(
            title=slide_data.title,
            content=slide_data.content,
            is_public=slide_data.is_public,
            owner_email=current_user.email,
            owner_username=current_user.username
        )

        saved_slide = await self.slide_repository.save(slide)

        return SlideResponseDTO(
            id=saved_slide.id.value,
            title=saved_slide.title,
            content=saved_slide.content,
            is_public=saved_slide.is_public,
            owner_email=saved_slide.owner_email,
            owner_username=saved_slide.owner_username,
            created_at=saved_slide.created_at,
            updated_at=saved_slide.updated_at
        )

    async def get_slides_by_user(self, user: User) -> List[SlideResponseDTO]:
        """ユーザーのスライドを取得する"""
        slides = await self.slide_repository.find_by_owner(user.id)

        return [
            SlideResponseDTO(
                id=slide.id.value,
                title=slide.title,
                content=slide.content,
                is_public=slide.is_public,
                owner_email=slide.owner_email,
                owner_username=slide.owner_username,
                created_at=slide.created_at,
                updated_at=slide.updated_at
            )
            for slide in slides
        ]

    async def get_public_slides(self) -> List[SlideResponseDTO]:
        """公開スライドを取得する"""
        slides = await self.slide_repository.find_public()

        return [
            SlideResponseDTO(
                id=slide.id.value,
                title=slide.title,
                content=slide.content,
                is_public=slide.is_public,
                owner_email=slide.owner_email,
                owner_username=slide.owner_username,
                created_at=slide.created_at,
                updated_at=slide.updated_at
            )
            for slide in slides
        ]

    async def get_slide_by_id(
        self, slide_id: int, current_user: Optional[User] = None
    ) -> Optional[SlideResponseDTO]:
        """IDによりスライドを取得する"""
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))

        if not slide:
            return None

        # 非公開スライドは所有者のみアクセス可能
        if not slide.is_public and (
            not current_user or slide.owner_email != current_user.email
        ):
            return None

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

    async def update_slide(
        self, slide_id: int, slide_data: SlideUpdateDTO, current_user: User
    ) -> Optional[SlideResponseDTO]:
        """スライドを更新する"""
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))

        if not slide:
            return None

        # 所有者のみ編集可能
        if slide.owner_email != current_user.email:
            return None

        slide.update(
            title=slide_data.title,
            content=slide_data.content,
            is_public=slide_data.is_public
        )

        updated_slide = await self.slide_repository.save(slide)

        return SlideResponseDTO(
            id=updated_slide.id.value,
            title=updated_slide.title,
            content=updated_slide.content,
            is_public=updated_slide.is_public,
            owner_email=updated_slide.owner_email,
            owner_username=updated_slide.owner_username,
            created_at=updated_slide.created_at,
            updated_at=updated_slide.updated_at
        )

    async def delete_slide(
        self, slide_id: int, current_user: User
    ) -> bool:
        """スライドを削除する"""
        slide = await self.slide_repository.find_by_id(SlideId(value=slide_id))

        if not slide:
            return False

        # 所有者のみ削除可能
        if slide.owner_email != current_user.email:
            return False

        return await self.slide_repository.delete(SlideId(value=slide_id))