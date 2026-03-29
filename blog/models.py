from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """ブログカテゴリ"""
    name = models.CharField('カテゴリ名', max_length=100, unique=True)
    slug = models.SlugField('スラッグ', max_length=100, unique=True)
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ブログタグ"""
    name = models.CharField('タグ名', max_length=50, unique=True)
    slug = models.SlugField('スラッグ', max_length=50, unique=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """ブログ投稿"""
    STATUS_CHOICES = [
        ('draft', '下書き'),
        ('published', '公開'),
    ]

    title = models.CharField('タイトル', max_length=200)
    body = models.TextField('本文')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='著者'
    )
    status = models.CharField(
        'ステータス',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='カテゴリ'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name='タグ'
    )
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    published_at = models.DateTimeField('公開日時', null=True, blank=True)

    class Meta:
        verbose_name = 'ブログ投稿'
        verbose_name_plural = 'ブログ投稿'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 公開ステータスに変更された場合、公開日時を設定
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
