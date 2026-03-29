#!/bin/bash

# エラーが発生したら即座に終了
set -e

# データベース接続待機
echo "Waiting for PostgreSQL..."
until python -c "import socket; socket.create_connection(('db', 5432), timeout=1)" 2>/dev/null; do
  echo "Waiting for database..."
  sleep 1
done
echo "PostgreSQL started"

# マイグレーション実行
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# 管理者ユーザー作成
echo "Creating admin user..."
python manage.py create_admin

# 静的ファイル収集(必要に応じて)
# python manage.py collectstatic --noinput

# 開発サーバー起動
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
