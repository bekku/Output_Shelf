# スライド管理アプリ

HTMLやSVG形式で記載されたコードベースのスライド情報を管理するWebアプリケーションです。

## 機能

- ユーザー登録・ログイン機能
- スライド作成・編集・削除機能
- スライドの公開/非公開設定
- 公開スライド一覧表示

## 技術スタック

### フロントエンド

- Next.js 15.2.2
- TypeScript
- Tailwind CSS
- ESLint

### バックエンド

- Python FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- JWT認証

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

2. Docker Composeでアプリケーションを起動

```bash
docker-compose up --build
```

3. ブラウザでアクセス

- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000

## テストアカウント

以下のアカウントでログインできます。

- メールアドレス: user@example.com
- パスワード: password

## API仕様

### 認証API

- POST /api/auth/register - ユーザー登録
- POST /api/auth/token - ログイン（トークン取得）
- GET /api/auth/me - 現在のユーザー情報取得

### スライドAPI

- GET /api/slides - スライド一覧取得
- POST /api/slides - スライド作成
- GET /api/slides/{id} - スライド詳細取得
- PUT /api/slides/{id} - スライド更新
- DELETE /api/slides/{id} - スライド削除
- GET /api/public-slides - 公開スライド一覧取得

## プロジェクト構成

```
.
├── backend/                  # バックエンドアプリケーション
│   ├── app/                  # アプリケーションコード
│   │   ├── api/              # API定義
│   │   │   └── routes/       # APIルート
│   │   ├── domain/           # ドメインロジック
│   │   ├── infrastructure/   # インフラストラクチャ層
│   │   └── application/      # アプリケーション層
│   ├── Dockerfile            # バックエンドのDockerfile
│   └── requirements.txt      # Pythonの依存関係
├── frontend/                 # フロントエンドアプリケーション
│   ├── src/                  # ソースコード
│   │   ├── app/              # Next.jsアプリケーション
│   │   │   ├── components/   # コンポーネント
│   │   │   ├── contexts/     # コンテキスト
│   │   │   └── ...           # 各ページ
│   ├── Dockerfile            # フロントエンドのDockerfile
│   └── package.json          # npmの依存関係
└── docker-compose.yml        # Docker Compose設定
```

## ライセンス

MIT