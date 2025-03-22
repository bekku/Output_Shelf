from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.infrastructure.database.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    slides = relationship("SlideModel", back_populates="owner")
    likes = relationship("LikeModel", back_populates="user", overlaps="liked_slides")
    liked_slides = relationship("SlideModel", secondary="likes", back_populates="liked_by_users", overlaps="likes")


class SlideModel(Base):
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
    liked_by_users = relationship("UserModel", secondary="likes", back_populates="liked_slides", overlaps="likes")
    like_details = relationship("LikeModel", back_populates="slide", overlaps="liked_by_users,liked_slides")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LikeModel(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    slide_id = Column(Integer, ForeignKey("slides.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('user_id', 'slide_id', name='unique_user_slide_like'),
    )

    user = relationship("UserModel", back_populates="likes", overlaps="liked_by_users,liked_slides")
    slide = relationship("SlideModel", back_populates="like_details", overlaps="liked_by_users,liked_slides")
