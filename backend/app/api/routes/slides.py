from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.application.interfaces.slide_dto import (
    SlideCreateDTO, SlideResponseDTO, SlideUpdateDTO
)
from app.application.use_cases.slide_use_cases import SlideUseCases
from app.api.routes.auth import get_current_user
from app.infrastructure.database.repositories.slide_repository_impl import (
    SlideRepositoryImpl
)
from app.infrastructure.database.database import get_db_session

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
    current_user=Depends(get_current_user),
    slide_use_cases: SlideUseCases=Depends(get_slide_use_cases)
):
    """スライドを作成する"""
    # ユースケースを使用してスライドを作成
    return await slide_use_cases.create_slide(slide_data, current_user)

@router.get("/slides", response_model=List[SlideResponseDTO])
async def read_slides(
    current_user=Depends(get_current_user),
    slide_use_cases: SlideUseCases=Depends(get_slide_use_cases)
):
    """ユーザーのスライドを取得する"""
    # ユースケースを使用してユーザーのスライドを取得
    return await slide_use_cases.get_slides_by_user(current_user)

@router.get("/slides/{slide_id}", response_model=SlideResponseDTO)
async def read_slide(
    slide_id: int,
    current_user=Depends(get_current_user),
    slide_use_cases: SlideUseCases=Depends(get_slide_use_cases)
):
    """IDによりスライドを取得する"""
    # ユースケースを使用してスライドを取得
    slide = await slide_use_cases.get_slide_by_id(slide_id, current_user)

    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")

    return slide

@router.put("/slides/{slide_id}", response_model=SlideResponseDTO)
async def update_slide(
    slide_id: int,
    slide_data: SlideUpdateDTO,
    current_user=Depends(get_current_user),
    slide_use_cases: SlideUseCases=Depends(get_slide_use_cases)
):
    """スライドを更新する"""
    # ユースケースを使用してスライドを更新
    updated_slide = await slide_use_cases.update_slide(
        slide_id, slide_data, current_user
    )

    if not updated_slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found or not authorized to update"
        )

    return updated_slide

@router.delete("/slides/{slide_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_slide(
    slide_id: int,
    current_user=Depends(get_current_user),
    slide_use_cases: SlideUseCases=Depends(get_slide_use_cases)
):
    """スライドを削除する"""
    # ユースケースを使用してスライドを削除
    success = await slide_use_cases.delete_slide(slide_id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found or not authorized to delete"
        )

    return None

@router.get("/public-slides", response_model=List[SlideResponseDTO])
async def read_public_slides(
    slide_use_cases: SlideUseCases=Depends(get_slide_use_cases)
):
    """公開スライドを取得する"""
    # ユースケースを使用して公開スライドを取得
    return await slide_use_cases.get_public_slides()