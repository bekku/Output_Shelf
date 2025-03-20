from pydantic import BaseModel, EmailStr


class TokenDTO(BaseModel):
    """トークンDTO"""
    access_token: str
    token_type: str


class UserBaseDTO(BaseModel):
    """ユーザー基本DTO"""
    email: EmailStr
    username: str


class UserCreateDTO(UserBaseDTO):
    """ユーザー作成DTO"""
    password: str


class UserResponseDTO(UserBaseDTO):
    """ユーザー応答DTO"""
    id: int
    class Config:
        from_attributes = True