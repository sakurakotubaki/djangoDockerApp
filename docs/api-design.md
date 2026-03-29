---
marp: true
theme: default
paginate: true
header: 'Django REST Framework ブログAPI'
footer: '© 2026 Engineer Blog API'
---

# Django REST Framework
## エンジニア向けブログAPI 設計書

Django REST Frameworkを使用したブログシステムの
API設計とデータベース設計

---

## 目次

1. プロジェクト概要
2. 技術スタック
3. 認証設計
4. データベース設計
5. APIエンドポイント一覧
6. 使用例
7. セットアップ手順

---

## 1. プロジェクト概要

### 目的
エンジニア向けの技術ブログシステムのバックエンドAPI

### 主な機能
- ✅ JWT + セッション認証
- ✅ ブログ投稿のCRUD操作
- ✅ カテゴリ・タグ管理
- ✅ 公開/下書きステータス管理
- ✅ Swagger UI による自動ドキュメント生成

---

## 2. 技術スタック

### バックエンド
- **Django 5.1** - Webフレームワーク
- **Django REST Framework 3.15** - REST API構築
- **PostgreSQL 16** - データベース
- **Docker + Docker Compose** - コンテナ化

### 認証・ドキュメント
- **djangorestframework-simplejwt** - JWT認証
- **drf-spectacular** - OpenAPI/Swagger生成
- **django-cors-headers** - CORS対応

---

## 3. 認証設計

### 認証方式

#### 1. JWT認証 (API用)
```
アクセストークン: 1時間有効
リフレッシュトークン: 7日有効
```

#### 2. セッション認証 (Browsable API用)
```
Django標準のセッション認証
開発・テスト用に使用
```

---

## 3. 認証設計 (続き)

### JWT取得フロー

```bash
# 1. トークン取得
POST /api/token/
{
  "username": "admin",
  "password": "adminpass"
}

# レスポンス
{
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc..."
}
```

---

## 3. 認証設計 (続き)

### JWT使用例

```bash
# 2. APIリクエスト時にアクセストークンを使用
GET /api/posts/
Authorization: Bearer eyJhbGc...

# 3. トークンリフレッシュ
POST /api/token/refresh/
{
  "refresh": "eyJhbGc..."
}
```

---

## 4. データベース設計

### モデル構成

```
User (Django標準)
  ↓ 1:N
BlogPost
  ↓ N:1        ↓ N:N
Category      Tag
```

---

## 4. データベース設計 (続き)

### BlogPost モデル

| フィールド | 型 | 説明 |
|----------|-----|------|
| id | Integer | 主キー(自動生成) |
| title | String(200) | タイトル |
| body | Text | 本文 |
| author | ForeignKey | 著者(User) |
| status | String | draft/published |
| category | ForeignKey | カテゴリ(NULL可) |
| tags | ManyToMany | タグ |
| created_at | DateTime | 作成日時 |
| updated_at | DateTime | 更新日時 |
| published_at | DateTime | 公開日時 |

---

## 4. データベース設計 (続き)

### Category モデル

| フィールド | 型 | 説明 |
|----------|-----|------|
| id | Integer | 主キー |
| name | String(100) | カテゴリ名 |
| slug | String(100) | スラッグ(URL用) |
| description | Text | 説明 |
| created_at | DateTime | 作成日時 |
| updated_at | DateTime | 更新日時 |

---

## 4. データベース設計 (続き)

### Tag モデル

| フィールド | 型 | 説明 |
|----------|-----|------|
| id | Integer | 主キー |
| name | String(50) | タグ名 |
| slug | String(50) | スラッグ(URL用) |
| created_at | DateTime | 作成日時 |

---

## 5. APIエンドポイント一覧

### 認証エンドポイント

| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| POST | /api/token/ | JWT取得 |
| POST | /api/token/refresh/ | トークンリフレッシュ |
| GET | /api-auth/login/ | セッションログイン |

---

## 5. APIエンドポイント一覧 (続き)

### ブログ投稿エンドポイント

| メソッド | エンドポイント | 認証 | 説明 |
|---------|--------------|------|------|
| GET | /api/posts/ | - | 投稿一覧(公開のみ) |
| POST | /api/posts/ | ✅ | 投稿作成 |
| GET | /api/posts/{id}/ | - | 投稿詳細 |
| PUT | /api/posts/{id}/ | ✅ | 投稿更新(著者のみ) |
| PATCH | /api/posts/{id}/ | ✅ | 投稿部分更新 |
| DELETE | /api/posts/{id}/ | ✅ | 投稿削除(著者のみ) |

---

## 5. APIエンドポイント一覧 (続き)

### カスタムアクション

| メソッド | エンドポイント | 認証 | 説明 |
|---------|--------------|------|------|
| GET | /api/posts/my_posts/ | ✅ | 自分の投稿一覧 |
| POST | /api/posts/{id}/publish/ | ✅ | 投稿を公開 |
| POST | /api/posts/{id}/draft/ | ✅ | 下書きに戻す |

---

## 5. APIエンドポイント一覧 (続き)

### カテゴリ・タグエンドポイント

| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| GET | /api/categories/ | カテゴリ一覧 |
| POST | /api/categories/ | カテゴリ作成 |
| GET | /api/categories/{slug}/ | カテゴリ詳細 |
| GET | /api/tags/ | タグ一覧 |
| POST | /api/tags/ | タグ作成 |

---

## 5. APIエンドポイント一覧 (続き)

### ドキュメントエンドポイント

| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| GET | /api/schema/ | OpenAPIスキーマ |
| GET | /api/docs/ | Swagger UI |
| GET | /api/redoc/ | Redoc |
| GET | /admin/ | Django管理画面 |

---

## 6. 使用例

### 投稿一覧の取得

```bash
curl http://localhost:8000/api/posts/

# レスポンス
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Django REST Frameworkの基礎",
      "excerpt": "DRFを使ったAPI開発について...",
      "author": {...},
      "status": "published",
      "created_at": "2026-03-29T09:56:07+09:00"
    }
  ]
}
```

---

## 6. 使用例 (続き)

### 投稿の作成

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django REST Frameworkの基礎",
    "body": "DRFを使ったAPI開発について解説します。",
    "status": "published"
  }'
```

---

## 6. 使用例 (続き)

### レスポンス例

```json
{
  "id": 1,
  "title": "Django REST Frameworkの基礎",
  "body": "DRFを使ったAPI開発について解説します。",
  "author": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "status": "published",
  "category": null,
  "tags": [],
  "created_at": "2026-03-29T09:56:07+09:00",
  "published_at": "2026-03-29T09:56:07+09:00"
}
```

---

## 7. セットアップ手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd djangoDockerApp
```

### 2. Dockerコンテナの起動

```bash
docker compose up --build
```

これで以下が自動実行されます:
- データベースマイグレーション
- 管理者ユーザー作成 (admin/adminpass)
- 開発サーバー起動

---

## 7. セットアップ手順 (続き)

### 3. アクセス確認

- **Browsable API**: http://localhost:8000/api/posts/
- **Swagger UI**: http://localhost:8000/api/docs/
- **Redoc**: http://localhost:8000/api/redoc/
- **管理画面**: http://localhost:8000/admin/

### 4. ログイン情報

```
ユーザー名: admin
パスワード: adminpass
```

---

## パフォーマンス最適化

### 実装済みの最適化

- **N+1問題の回避**
  - `select_related('author', 'category')`
  - `prefetch_related('tags')`

- **データベースインデックス**
  - `created_at`, `status` にインデックス設定

- **ページネーション**
  - 10件/ページで自動ページング

- **軽量シリアライザー**
  - 一覧用と詳細用でシリアライザーを分離

---

## セキュリティ対策

### 実装済みのセキュリティ機能

- **JWT認証**
  - アクセストークン: 1時間
  - リフレッシュトークン: 7日

- **権限管理**
  - 著者のみ編集・削除可能
  - 読み取りは全員許可

- **CORS設定**
  - localhost:3000のみ許可

- **環境変数管理**
  - SECRET_KEY, DATABASE_URL

---

## アーキテクチャの特徴

### DRFのベストプラクティス

```
ViewSet + Router
  ↓
自動的にCRUDエンドポイント生成
  ↓
少ないコードで実装完了
```

### 主なコンポーネント
- **Serializer**: データ変換・バリデーション
- **ViewSet**: ビジネスロジック
- **Permission**: 権限管理
- **Router**: URLルーティング自動生成

---

## 拡張可能な機能

### 将来的に追加可能

- コメント機能
- いいね機能
- 画像アップロード
- 検索機能の強化 (Elasticsearch)
- ドラフト自動保存
- 記事公開予約
- 閲覧数カウント
- RSS/Atomフィード
- メール通知

---

## まとめ

### 主な実装内容

✅ JWT + セッション認証
✅ BlogPost, Category, Tag モデル
✅ ViewSetによるCRUD API
✅ パフォーマンス最適化
✅ Swagger UI自動生成
✅ Docker環境構築

### 技術的な特徴

- 少ないコードで高機能
- スケーラブルな設計
- セキュアな認証
- 優れた開発体験

---

## ご質問・お問い合わせ

### リソース

- **GitHub**: <repository-url>
- **Swagger UI**: http://localhost:8000/api/docs/
- **Django管理画面**: http://localhost:8000/admin/

### ドキュメント

- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- drf-spectacular: https://drf-spectacular.readthedocs.io/

---

# ありがとうございました

## Django REST Framework
### エンジニア向けブログAPI

質問はありますか?
