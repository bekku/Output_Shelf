from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

from app.application.interfaces.user_dto import (
    UserCreateDTO, UserResponseDTO, TokenDTO
)
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.domain.services.auth_service import AuthService
from app.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl
)
from app.infrastructure.database.database import get_db_session

router = APIRouter()

# セキュリティ設定
SECRET_KEY = ("09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
              )  # 本番環境では環境変数から取得
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


# 依存性注入関数
async def get_auth_use_cases(db=Depends(get_db_session)):
    """AuthUseCasesのインスタンスを取得する依存性注入関数"""
    user_repository = UserRepositoryImpl(db)
    auth_service = AuthService(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return AuthUseCases(user_repository, auth_service)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    """現在のユーザーを取得する依存性注入関数"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # JWTトークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # ユースケースを使用してユーザーを取得
    user = await auth_use_cases.get_current_user(email)
    if user is None:
        raise credentials_exception

    return user


# ルート定義
@router.post("/auth/token", response_model=TokenDTO)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    """ユーザー認証とアクセストークン発行"""
    # ユースケースを使用して認証
    token = await auth_use_cases.authenticate_user(
        email=form_data.username,  # OAuth2のフォームではusernameフィールドを使用
        password=form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


@router.post("/auth/register", response_model=UserResponseDTO)
async def register_user(
    user_data: UserCreateDTO,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    """ユーザー登録"""
    # ユースケースを使用してユーザーを登録
    user = await auth_use_cases.register_user(user_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return user


@router.get("/auth/me", response_model=UserResponseDTO)
async def read_users_me(
    current_user: UserResponseDTO = Depends(get_current_user)
):
    """現在のユーザー情報を取得"""
    return current_user