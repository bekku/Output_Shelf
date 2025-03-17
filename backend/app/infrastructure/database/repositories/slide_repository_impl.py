from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.slide import Slide, SlideId
from app.domain.entities.user import UserId
from app.domain.repositories.slide_repository import SlideRepository
from app.infrastructure.database.models import SlideModel


class SlideRepositoryImpl(SlideRepository):
    """スライドリポジトリの実装"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, slide: Slide) -> Slide:
        """スライドを保存する"""
        if slide.id is None:
            # 新規作成
            db_slide = SlideModel(
                title=slide.title,
                content=slide.content,
                is_public=slide.is_public,
                owner_email=slide.owner_email,
                owner_username=slide.owner_username
            )
            self.session.add(db_slide)
            await self.session.flush()
            await self.session.refresh(db_slide)

            # エンティティに変換して返す
            return Slide(
                id=SlideId(value=db_slide.id),
                title=db_slide.title,
                content=db_slide.content,
                is_public=db_slide.is_public,
                owner_email=db_slide.owner_email,
                owner_username=db_slide.owner_username,
                created_at=db_slide.created_at,
                updated_at=db_slide.updated_at
            )
        else:
            # 更新
            stmt = select(SlideModel).where(SlideModel.id == slide.id.value)
            result = await self.session.execute(stmt)
            db_slide = result.scalars().first()

            if db_slide:
                db_slide.title = slide.title
                db_slide.content = slide.content
                db_slide.is_public = slide.is_public
                db_slide.updated_at = datetime.utcnow()

                await self.session.flush()
                await self.session.refresh(db_slide)

                # エンティティに変換して返す
                return Slide(
                    id=SlideId(value=db_slide.id),
                    title=db_slide.title,
                    content=db_slide.content,
                    is_public=db_slide.is_public,
                    owner_email=db_slide.owner_email,
                    owner_username=db_slide.owner_username,
                    created_at=db_slide.created_at,
                    updated_at=db_slide.updated_at
                )

            return slide

    async def find_by_id(self, slide_id: SlideId) -> Optional[Slide]:
        """IDによりスライドを検索する"""
        stmt = select(SlideModel).where(SlideModel.id == slide_id.value)
        result = await self.session.execute(stmt)
        db_slide = result.scalars().first()

        if not db_slide:
            return None

        # エンティティに変換して返す
        return Slide(
            id=SlideId(value=db_slide.id),
            title=db_slide.title,
            content=db_slide.content,
            is_public=db_slide.is_public,
            owner_email=db_slide.owner_email,
            owner_username=db_slide.owner_username,
            created_at=db_slide.created_at,
            updated_at=db_slide.updated_at
        )

    async def find_by_owner(self, owner_id: UserId) -> List[Slide]:
        """所有者によりスライドを検索する"""
        stmt = select(SlideModel).where(
            SlideModel.owner_email == owner_id.value
        )
        result = await self.session.execute(stmt)
        db_slides = result.scalars().all()

        # エンティティに変換して返す
        return [
            Slide(
                id=SlideId(value=db_slide.id),
                title=db_slide.title,
                content=db_slide.content,
                is_public=db_slide.is_public,
                owner_email=db_slide.owner_email,
                owner_username=db_slide.owner_username,
                created_at=db_slide.created_at,
                updated_at=db_slide.updated_at
            )
            for db_slide in db_slides
        ]

    async def find_public(self) -> List[Slide]:
        """公開スライドを検索する"""
        stmt = select(SlideModel).where(SlideModel.is_public.is_(True))
        result = await self.session.execute(stmt)
        db_slides = result.scalars().all()

        # エンティティに変換して返す
        return [
            Slide(
                id=SlideId(value=db_slide.id),
                title=db_slide.title,
                content=db_slide.content,
                is_public=db_slide.is_public,
                owner_email=db_slide.owner_email,
                owner_username=db_slide.owner_username,
                created_at=db_slide.created_at,
                updated_at=db_slide.updated_at
            )
            for db_slide in db_slides
        ]

    async def delete(self, slide_id: SlideId) -> bool:
        """スライドを削除する"""
        stmt = select(SlideModel).where(SlideModel.id == slide_id.value)
        result = await self.session.execute(stmt)
        db_slide = result.scalars().first()

        if not db_slide:
            return False

        await self.session.delete(db_slide)
        await self.session.flush()

        return True