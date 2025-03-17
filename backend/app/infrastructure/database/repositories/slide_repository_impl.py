from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

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
            await self.session.commit()
            await self.session.refresh(db_slide)
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
                await self.session.commit()
                await self.session.refresh(db_slide)
            else:
                return slide

        # エンティティに変換して返す
        return self._to_entity(db_slide)

    async def find_by_id(self, slide_id: SlideId) -> Optional[Slide]:
        """IDによりスライドを検索する"""
        stmt = select(SlideModel).where(SlideModel.id == slide_id.value)
        result = await self.session.execute(stmt)
        db_slide = result.scalars().first()

        if not db_slide:
            return None

        # エンティティに変換して返す
        return self._to_entity(db_slide)

    async def find_by_owner(self, owner_id: UserId) -> List[Slide]:
        """所有者によりスライドを検索する"""
        stmt = select(SlideModel).where(
            SlideModel.owner_email == owner_id.value
        )
        result = await self.session.execute(stmt)
        db_slides = result.scalars().all()

        # エンティティに変換して返す
        return [self._to_entity(db_slide) for db_slide in db_slides]

    async def find_public(
        self, page: int = 1, per_page: int = 18
    ) -> Tuple[List[Slide], int]:
        """公開スライドを検索する（ページネーション付き）"""
        # 総件数を取得
        count_query = select(func.count()).select_from(SlideModel).where(
            SlideModel.is_public == True
        )
        total_count = await self.session.scalar(count_query)
        total_pages = (total_count + per_page - 1) // per_page

        # ページネーション付きでスライドを取得
        query = (
            select(SlideModel)
            .where(SlideModel.is_public == True)
            .order_by(SlideModel.updated_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = await self.session.execute(query)
        db_slides = result.scalars().all()
        return [self._to_entity(db_slide) for db_slide in db_slides], total_pages

    async def delete(self, slide_id: SlideId) -> bool:
        """スライドを削除する"""
        stmt = select(SlideModel).where(SlideModel.id == slide_id.value)
        result = await self.session.execute(stmt)
        db_slide = result.scalars().first()

        if not db_slide:
            return False

        await self.session.delete(db_slide)
        await self.session.commit()

        return True

    def _to_entity(self, db_slide: SlideModel) -> Slide:
        """DBモデルからエンティティに変換する"""
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