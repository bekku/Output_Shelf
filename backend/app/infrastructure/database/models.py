from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.infrastructure.database.database import Base


class UserModel(Base):
    """ユーザーのデータベースモデル"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    slides = relationship("SlideModel", back_populates="owner")
    likes = relationship("LikeModel", back_populates="user")
    liked_slides = relationship("SlideModel", secondary="likes", back_populates="liked_by_users")


class SlideModel(Base):
    """スライドのデータベースモデル"""
    __tablename__ = "slides"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_public = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner_username = Column(String, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    views = Column(Integer, default=0, nullable=False)

    owner = relationship("UserModel", back_populates="slides")
    liked_by_users = relationship("UserModel", secondary="likes", back_populates="liked_slides")
    like_details = relationship(
        "LikeModel",
        back_populates="slide",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=None  # onupdateを削除
    )


class LikeModel(Base):
    """ユーザーのいいねを管理するデータベースモデル"""
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    slide_id = Column(Integer, ForeignKey("slides.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ユニーク制約: 同じユーザーが同じスライドに複数回いいねできないようにする
    __table_args__ = (
        UniqueConstraint('user_id', 'slide_id', name='unique_user_slide_like'),
    )

    user = relationship("UserModel", back_populates="likes")
    slide = relationship("SlideModel", back_populates="like_details")
