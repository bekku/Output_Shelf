from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from app.domain.entities.slide import Slide
from app.domain.repositories.slide_repository import SlideRepository
from app.infrastructure.database.models import SlideModel, LikeModel


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
                id=slide.id,
                content=slide.content,
                is_public=slide.is_public,
                likes=0,
                views=0,
                owner_id=slide.owner_id,
                owner_username=slide.owner_username
            )
            self.session.add(db_slide)
            await self.session.commit()
            await self.session.refresh(db_slide)
        else:
            # 更新
            stmt = select(SlideModel).where(SlideModel.id == slide.id)
            result = await self.session.execute(stmt)
            db_slide = result.scalars().first()

            if db_slide:
                db_slide.title = slide.title
                db_slide.content = slide.content
                db_slide.is_public = slide.is_public
                db_slide.likes = slide.likes
                db_slide.views = slide.views
                db_slide.updated_at = datetime.utcnow()
                await self.session.commit()
                await self.session.refresh(db_slide)
            else:
                return slide

        # エンティティに変換して返す
        return self._to_entity(db_slide)

    async def find_by_id(self, slide_id: int) -> Optional[Slide]:
        """IDによりスライドを検索する"""
        stmt = select(SlideModel).where(SlideModel.id == slide_id)
        result = await self.session.execute(stmt)
        db_slide = result.scalars().first()

        if not db_slide:
            return None

        # エンティティに変換して返す
        return self._to_entity(db_slide)

    async def find_by_owner(
        self,
        owner_id: int,
        sort_by: str = "created_at"
    ) -> List[Slide]:
        """所有者によりスライドを検索する"""
        # ソート条件の設定
        if sort_by == "likes":
            order_by = SlideModel.likes.desc()
        elif sort_by == "views":
            order_by = SlideModel.views.desc()
        else:  # "created_at"がデフォルト
            order_by = SlideModel.created_at.desc()

        stmt = (
            select(SlideModel)
            .where(SlideModel.owner_id == owner_id)
            .order_by(order_by)
        )
        result = await self.session.execute(stmt)
        db_slides = result.scalars().all()

        return [self._to_entity(db_slide) for db_slide in db_slides]

    async def find_public(
        self,
        page: int = 1,
        per_page: int = 18,
        sort_by: str = "created_at"  # 新しいパラメータを追加
    ) -> Tuple[List[Slide], int]:
        """公開スライドを検索する（ページネーション付き）"""
        # 総件数を取得
        count_query = select(func.count()).select_from(SlideModel).where(
            SlideModel.is_public == True
        )
        total_count = await self.session.scalar(count_query)
        total_pages = (total_count + per_page - 1) // per_page

        # ソート条件の設定
        if sort_by == "likes":
            order_by = SlideModel.likes.desc()
        elif sort_by == "views":
            order_by = SlideModel.views.desc()
        else:  # "created_at"がデフォルト
            order_by = SlideModel.created_at.desc()

        # ページネーション付きでスライドを取得
        query = (
            select(SlideModel)
            .where(SlideModel.is_public == True)
            .order_by(order_by)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = await self.session.execute(query)
        db_slides = result.scalars().all()
        return [self._to_entity(db_slide) for db_slide in db_slides], total_pages

    async def delete(self, slide_id: int) -> bool:
        """スライドを削除する"""
        try:
            # まず、関連するいいねを削除
            delete_likes = delete(LikeModel).where(LikeModel.slide_id == slide_id)
            await self.session.execute(delete_likes)

            # 次に、スライドを削除
            stmt = select(SlideModel).where(SlideModel.id == slide_id)
            result = await self.session.execute(stmt)
            db_slide = result.scalars().first()

            if not db_slide:
                return False

            await self.session.delete(db_slide)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error deleting slide: {e}")
            return False

    async def toggle_like(self, slide_id: int, user_id: int) -> bool:
        """いいねを切り替える"""
        # 既存のいいねを確認
        stmt = select(LikeModel).where(
            LikeModel.slide_id == slide_id,
            LikeModel.user_id == user_id
        )
        result = await self.session.execute(stmt)
        existing_like = result.scalars().first()

        slide_stmt = select(SlideModel).where(SlideModel.id == slide_id)
        slide_result = await self.session.execute(slide_stmt)
        slide = slide_result.scalars().first()

        if not slide:
            return False

        if existing_like:
            # いいねを解除
            await self.session.delete(existing_like)
            slide.likes = max(0, slide.likes - 1)
            liked = False
        else:
            # いいねを追加
            new_like = LikeModel(user_id=user_id, slide_id=slide_id)
            self.session.add(new_like)
            slide.likes = slide.likes + 1
            liked = True

        await self.session.commit()
        return liked

    async def increment_view(self, slide_id: int) -> None:
        """閲覧数をインクリメントする（更新時間は変更しない）"""
        stmt = select(SlideModel).where(SlideModel.id == slide_id)
        result = await self.session.execute(stmt)
        slide = result.scalars().first()

        if slide:
            # viewsのみを更新し、updated_atは更新しない
            slide.views = slide.views + 1
            await self.session.commit()

    def _to_entity(self, db_slide: SlideModel) -> Slide:
        """DBモデルからエンティティに変換する"""
        return Slide(
            id=db_slide.id,
            title=db_slide.title,
            content=db_slide.content,
            is_public=db_slide.is_public,
            owner_id=db_slide.owner_id,
            owner_username=db_slide.owner_username,
            likes=db_slide.likes,
            views=db_slide.views,
            created_at=db_slide.created_at,
            updated_at=db_slide.updated_at
        )