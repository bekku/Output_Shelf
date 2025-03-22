# スライド管理アプリ

HTMLやSVG形式で記載されたコードベースのスライド情報を管理するWebアプリケーションです。

## 機能

- ユーザー登録・ログイン機能
- スライド作成・編集・削除機能
- スライドの公開/非公開設定
- 公開スライド一覧表示
- スライドのプレビュー機能
- ページネーション機能（1ページあたり18件表示）

## 技術スタック

### フロントエンド

- Next.js 15.2.2
- TypeScript
- Tailwind CSS
- ESLint
- React Context API（認証状態管理）

### バックエンド

- Python FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- JWT認証
- Clean Architecture

### インフラ

- Docker
- Docker Compose

## 開発環境のセットアップ

### 前提条件

- Docker
- Docker Compose

### 起動方法

1. リポジトリをクローン

```bash
git clone <repository-url>
cd <repository-directory>
```

2. 環境変数の設定

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:postgres@db:5432/slides
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Docker Composeでアプリケーションを起動

```bash
docker compose up --build
```

または、バックグラウンドで実行する場合:

```bash
docker compose up -d
```

開発中は通常これだけで十分です。ソースコードに変更を加えた場合は自動的に反映されます。
ただし、依存関係を変更した場合は再ビルドが必要です:

```bash
docker compose down
docker compose build
docker compose up -d
```

4. ブラウザでアクセス

- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000

## 本番環境デプロイ

本番環境にデプロイする場合は、以下の点に注意してください。

### 環境変数設定

本番環境では、実際のAPIエンドポイントを使用するため、環境変数`API_URL`を設定します:

```bash
# 例：実際の本番APIのURLを指定してビルド・起動
API_URL=https://api.example.com docker compose up -d
```

### セキュリティ上の注意点

1. 本番環境ではHTTPS通信を使用することを強く推奨します
2. `.env`ファイルには強力なシークレットキーを設定してください
3. 認証情報やAPIキーは環境変数または安全な認証情報管理ツールを使用して管理してください

### 本番環境向け追加設定

- リバースプロキシ (Nginx等) の使用を検討
- ログ管理やエラー監視ツールとの統合
- データベースのバックアップ定期実行

## テストアカウント

以下のアカウントでログインできます。

- メールアドレス: user@example.com
- パスワード: password

## API仕様

### 認証API

#### ユーザー登録
- **エンドポイント**: `POST /api/auth/register`
- **認証**: 不要
- **リクエストボディ**:
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password"
  }
  ```
- **レスポンス**: `UserResponseDTO`
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "username"
  }
  ```
- **エラー**:
  - 400: メールアドレスが既に登録されている場合

#### ログイン（トークン取得）
- **エンドポイント**: `POST /api/auth/token`
- **認証**: 不要
- **リクエストボディ**:
  ```json
  {
    "username": "user@example.com",
    "password": "password"
  }
  ```
- **レスポンス**: `TokenDTO`
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
  }
  ```
- **エラー**:
  - 401: メールアドレスまたはパスワードが正しくない場合

#### 現在のユーザー情報取得
- **エンドポイント**: `GET /api/auth/me`
- **認証**: 必須（Bearer Token）
- **ヘッダー**:
  - `Authorization: Bearer <access_token>`
- **レスポンス**: `UserResponseDTO`
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "username"
  }
  ```
- **エラー**:
  - 401: 認証情報が無効な場合

### スライド関連のエンドポイント

#### スライド作成
- **エンドポイント**: `POST /api/slides`
- **認証**: 必須
- **リクエストボディ**:
  ```json
  {
    "title": "スライドタイトル",
    "content": "スライドの内容",
    "is_public": true
  }
  ```
- **レスポンス**: `SlideResponseDTO`

#### スライド取得
- **エンドポイント**: `GET /api/slides/{slide_id}`
- **認証**: 不要
- **パスパラメータ**: `slide_id`（スライドID）
- **レスポンス**: `SlideResponseDTO`
- **エラー**:
  - 404: スライドが見つからない場合

#### ユーザーのスライド一覧取得
- **エンドポイント**: `GET /api/slides`
- **認証**: 必須
- **クエリパラメータ**:
  - `page`: ページ番号（デフォルト: 1）
  - `per_page`: 1ページあたりの表示数（デフォルト: 18, 最大: 100）
  - `sort_by`: ソート基準（`created_at`, `likes`, `views`）
- **レスポンス**: `Tuple[List[SlideResponseDTO], int]`（スライド一覧と総数）

#### 公開スライド一覧取得
- **エンドポイント**: `GET /api/public-slides`
- **認証**: 不要
- **クエリパラメータ**:
  - `page`: ページ番号（デフォルト: 1）
  - `per_page`: 1ページあたりの表示数（デフォルト: 18, 最大: 100）
  - `sort_by`: ソート基準（`created_at`, `likes`, `views`）
- **レスポンス**: `Tuple[List[SlideResponseDTO], int]`（スライド一覧と総数）

#### スライド更新
- **エンドポイント**: `PUT /api/slides/{slide_id}`
- **認証**: 必須（スライドの所有者のみ）
- **パスパラメータ**: `slide_id`（スライドID）
- **リクエストボディ**:
  ```json
  {
    "title": "更新後のタイトル",
    "content": "更新後の内容",
    "is_public": true
  }
  ```
- **レスポンス**: `SlideResponseDTO`
- **エラー**:
  - 403: 権限がない場合
  - 404: スライドが見つからない場合

#### スライド削除
- **エンドポイント**: `DELETE /api/slides/{slide_id}`
- **認証**: 必須（スライドの所有者のみ）
- **パスパラメータ**: `slide_id`（スライドID）
- **レスポンス**: `{ "message": "Slide deleted successfully" }`
- **エラー**:
  - 403: 権限がない場合
  - 404: スライドが見つからない場合
  - 500: 削除に失敗した場合

#### スライドへのいいね
- **エンドポイント**: `POST /api/slides/{slide_id}/like`
- **認証**: 必須
- **パスパラメータ**: `slide_id`（スライドID）
- **レスポンス**: `{ "liked": boolean }`

#### スライドの閲覧数増加
- **エンドポイント**: `POST /api/slides/{slide_id}/view`
- **認証**: 不要
- **パスパラメータ**: `slide_id`（スライドID）
- **レスポンス**: `{ "message": "View count incremented" }`

## プロジェクト構成

```
.
├── backend/                  # バックエンドアプリケーション
│   ├── app/                  # アプリケーションコード
│   │   ├── api/              # API定義
│   │   │   └── routes/       # APIルート
│   │   │       ├── auth.py   # 認証関連API
│   │   │       └── slides.py # スライド関連API
│   │   ├── domain/           # ドメインロジック
│   │   │   ├── entities/     # エンティティ
│   │   │   │   ├── slide.py  # スライドエンティティ
│   │   │   │   └── user.py   # ユーザーエンティティ
│   │   │   └── repositories/ # リポジトリインターフェース
│   │   ├── infrastructure/   # インフラストラクチャ層
│   │   │   └── database/     # データベース関連
│   │   │       ├── models.py # データベースモデル
│   │   │       └── repositories/ # リポジトリ実装
│   │   └── application/      # アプリケーション層
│   │       └── use_cases/    # ユースケース
│   ├── Dockerfile            # バックエンドのDockerfile
│   └── requirements.txt      # Pythonの依存関係
├── frontend/                 # フロントエンドアプリケーション
│   ├── src/                  # ソースコード
│   │   ├── app/              # Next.jsアプリケーション
│   │   │   ├── components/   # コンポーネント
│   │   │   │   ├── Pagination.tsx
│   │   │   │   └── SlidePreview.tsx
│   │   │   ├── contexts/     # コンテキスト
│   │   │   │   └── AuthContext.tsx
│   │   │   └── ...           # 各ページ
│   ├── Dockerfile            # フロントエンドのDockerfile
│   └── package.json          # npmの依存関係
└── docker-compose.yml        # Docker Compose設定
```

## ライセンス

MIT