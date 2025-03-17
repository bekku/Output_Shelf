from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Tuple

from app.application.interfaces.slide_dto import (
    SlideCreateDTO, SlideResponseDTO, SlideUpdateDTO
)
from app.application.use_cases.slide_use_cases import SlideUseCases
from app.domain.repositories.slide_repository import SlideRepository
from app.infrastructure.database.repositories.slide_repository_impl import (
    SlideRepositoryImpl
)
from app.infrastructure.database.database import get_db_session
from app.api.routes.auth import get_current_user

router = APIRouter()

# 依存性注入関数
async def get_slide_use_cases(db=Depends(get_db_session)):
    """SlideUseCasesのインスタンスを取得する依存性注入関数"""
    slide_repository = SlideRepositoryImpl(db)
    return SlideUseCases(slide_repository)

# ルート定義
@router.post("/slides", response_model=SlideResponseDTO)
async def create_slide(
    slide_data: SlideCreateDTO,
    current_user = Depends(get_current_user),
    slide_use_cases: SlideUseCases = Depends(get_slide_use_cases)
):
    """スライドを作成する"""
    slide = await slide_use_cases.create_slide(
        slide_data=slide_data,
        current_user=current_user
    )
    return slide

@router.get("/slides/{slide_id}", response_model=SlideResponseDTO)
async def get_slide(
    slide_id: str,
    slide_use_cases: SlideUseCases = Depends(get_slide_use_cases)
):
    """スライドを取得する"""
    slide = await slide_use_cases.get_slide(slide_id)
    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )
    return slide

@router.get("/slides", response_model=Tuple[List[SlideResponseDTO], int])
async def get_user_slides(
    page: int = Query(1, ge=1, description="ページ番号"),
    per_page: int = Query(18, ge=1, le=100, description="1ページあたりの表示数"),
    current_user = Depends(get_current_user),
    slide_use_cases: SlideUseCases = Depends(get_slide_use_cases)
):
    """ユーザーのスライドを取得する（ページネーション付き）"""
    return await slide_use_cases.get_user_slides(
        owner_email=current_user.email,
        page=page,
        per_page=per_page
    )

@router.get("/public-slides", response_model=Tuple[List[SlideResponseDTO], int])
async def get_public_slides(
    page: int = Query(1, ge=1, description="ページ番号"),
    per_page: int = Query(18, ge=1, le=100, description="1ページあたりの表示数"),
    slide_use_cases: SlideUseCases = Depends(get_slide_use_cases)
):
    """公開スライドを取得する（ページネーション付き）"""
    return await slide_use_cases.get_public_slides(page=page, per_page=per_page)

@router.put("/slides/{slide_id}", response_model=SlideResponseDTO)
async def update_slide(
    slide_id: str,
    slide_data: SlideUpdateDTO,
    current_user = Depends(get_current_user),
    slide_use_cases: SlideUseCases = Depends(get_slide_use_cases)
):
    """スライドを更新する"""
    slide = await slide_use_cases.get_slide(slide_id)
    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )
    if slide.owner_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    updated_slide = await slide_use_cases.update_slide(slide_id, slide_data)
    return updated_slide

@router.delete("/slides/{slide_id}")
async def delete_slide(
    slide_id: str,
    current_user = Depends(get_current_user),
    slide_use_cases: SlideUseCases = Depends(get_slide_use_cases)
):
    """スライドを削除する"""
    slide = await slide_use_cases.get_slide(slide_id)
    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )
    if slide.owner_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    success = await slide_use_cases.delete_slide(slide_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete slide"
        )
    return {"message": "Slide deleted successfully"}