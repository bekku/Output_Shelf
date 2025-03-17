from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.api.routes.auth import User, get_current_user

router = APIRouter()

# 仮のスライドデータベース（実際の実装ではデータベースを使用）
fake_slides_db = {}
slide_id_counter = 1

# モデル定義
class SlideBase(BaseModel):
    title: str
    content: str  # HTML or SVG content
    is_public: bool = True

class SlideCreate(SlideBase):
    pass

class Slide(SlideBase):
    id: int
    owner_email: str
    owner_username: str
    created_at: datetime
    updated_at: datetime

# ルート定義
@router.post("/slides", response_model=Slide)
async def create_slide(
    slide: SlideCreate, current_user: User = Depends(get_current_user)
):
    global slide_id_counter
    now = datetime.utcnow()
    new_slide = Slide(
        id=slide_id_counter,
        owner_email=current_user.email,
        owner_username=current_user.username,
        created_at=now,
        updated_at=now,
        **slide.dict()
    )
    fake_slides_db[slide_id_counter] = new_slide
    slide_id_counter += 1
    return new_slide

@router.get("/slides", response_model=List[Slide])
async def read_slides(current_user: User = Depends(get_current_user)):
    # ユーザーが所有するスライドと公開スライドを取得
    return [
        slide for slide in fake_slides_db.values()
        if slide.owner_email == current_user.email or slide.is_public
    ]

@router.get("/slides/{slide_id}", response_model=Slide)
async def read_slide(slide_id: int, current_user: User = Depends(get_current_user)):
    if slide_id not in fake_slides_db:
        raise HTTPException(status_code=404, detail="Slide not found")

    slide = fake_slides_db[slide_id]
    # 非公開スライドは所有者のみアクセス可能
    if not slide.is_public and slide.owner_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this slide"
        )
    return slide

@router.put("/slides/{slide_id}", response_model=Slide)
async def update_slide(
    slide_id: int, slide_update: SlideCreate, current_user: User = Depends(get_current_user)
):
    if slide_id not in fake_slides_db:
        raise HTTPException(status_code=404, detail="Slide not found")

    slide = fake_slides_db[slide_id]
    # 所有者のみ編集可能
    if slide.owner_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this slide"
        )

    update_data = slide_update.dict()
    for key, value in update_data.items():
        setattr(slide, key, value)

    slide.updated_at = datetime.utcnow()
    fake_slides_db[slide_id] = slide
    return slide

@router.delete("/slides/{slide_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_slide(slide_id: int, current_user: User = Depends(get_current_user)):
    if slide_id not in fake_slides_db:
        raise HTTPException(status_code=404, detail="Slide not found")

    slide = fake_slides_db[slide_id]
    # 所有者のみ削除可能
    if slide.owner_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this slide"
        )

    del fake_slides_db[slide_id]
    return None

@router.get("/public-slides", response_model=List[Slide])
async def read_public_slides():
    # 公開スライドのみを取得（認証不要）
    return [slide for slide in fake_slides_db.values() if slide.is_public]