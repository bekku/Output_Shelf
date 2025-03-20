from datetime import datetime
from pydantic import BaseModel


class SlideBaseDTO(BaseModel):
    """スライド基本DTO"""
    title: str
    content: str
    is_public: bool = True


class SlideCreateDTO(SlideBaseDTO):
    """スライド作成DTO"""
    likes: int = 0
    views: int = 0
    pass


class SlideUpdateDTO(SlideBaseDTO):
    """スライド更新DTO"""
    pass


class SlideResponseDTO(SlideBaseDTO):
    """スライド応答DTO"""
    id: int
    title: str
    content: str
    owner_id: int
    owner_username: str
    likes: int
    views: int
    created_at: datetime
    updated_at: datetime
    is_public: bool

    class Config:
        from_attributes = True