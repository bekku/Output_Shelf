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
docker-compose up --build
```

4. ブラウザでアクセス

- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000

## テストアカウント

以下のアカウントでログインできます。

- メールアドレス: user@example.com
- パスワード: password

## API仕様

### 認証API

- POST /api/auth/register - ユーザー登録
  - リクエスト: `{ "email": string, "username": string, "password": string }`
  - レスポンス: `{ "id": number, "email": string, "username": string }`
- POST /api/auth/token - ログイン（トークン取得）
  - リクエスト: `{ "username": string, "password": string }`
  - レスポンス: `{ "access_token": string, "token_type": "bearer" }`
- GET /api/auth/me - 現在のユーザー情報取得
  - レスポンス: `{ "id": number, "email": string, "username": string }`

### スライドAPI

- GET /api/slides - スライド一覧取得（ページネーション対応）
  - クエリパラメータ: `page`（デフォルト: 1）
  - レスポンス: `{ "slides": Slide[], "total_pages": number }`
- POST /api/slides - スライド作成
  - リクエスト: `{ "title": string, "content": string, "is_public": boolean }`
  - レスポンス: `Slide`
- GET /api/slides/{id} - スライド詳細取得
  - レスポンス: `Slide`
- PUT /api/slides/{id} - スライド更新
  - リクエスト: `{ "title": string, "content": string, "is_public": boolean }`
  - レスポンス: `Slide`
- DELETE /api/slides/{id} - スライド削除
  - レスポンス: `{ "message": "Slide deleted successfully" }`
- GET /api/public-slides - 公開スライド一覧取得（ページネーション対応）
  - クエリパラメータ: `page`（デフォルト: 1）
  - レスポンス: `{ "slides": Slide[], "total_pages": number }`

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