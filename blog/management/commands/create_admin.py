from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = '管理者ユーザーを作成します'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'adminpass'
        email = 'admin@example.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'管理者ユーザー "{username}" は既に存在します')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'管理者ユーザー "{username}" を作成しました')
            )
            self.stdout.write(
                self.style.SUCCESS(f'ユーザー名: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'パスワード: {password}')
            )
