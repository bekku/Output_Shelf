from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String, Text)
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


class SlideModel(Base):
    """スライドのデータベースモデル"""
    __tablename__ = "slides"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_public = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner_username = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)

    owner = relationship("UserModel", back_populates="slides")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
