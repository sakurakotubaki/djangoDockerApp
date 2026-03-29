from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import BlogPost, Category, Tag
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    CategorySerializer,
    TagSerializer
)
from .permissions import IsAuthorOrReadOnly


@extend_schema_view(
    list=extend_schema(description='ブログ投稿一覧を取得', tags=['Blog Posts']),
    retrieve=extend_schema(description='ブログ投稿詳細を取得', tags=['Blog Posts']),
    create=extend_schema(description='ブログ投稿を作成', tags=['Blog Posts']),
    update=extend_schema(description='ブログ投稿を更新', tags=['Blog Posts']),
    partial_update=extend_schema(description='ブログ投稿を部分更新', tags=['Blog Posts']),
    destroy=extend_schema(description='ブログ投稿を削除', tags=['Blog Posts']),
)
class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ブログ投稿のCRUD操作を提供するViewSet

    - list: 投稿一覧取得(公開済み投稿のみ)
    - retrieve: 投稿詳細取得
    - create: 投稿作成(認証必須)
    - update/partial_update: 投稿更新(著者のみ)
    - destroy: 投稿削除(著者のみ)
    - my_posts: 自分の投稿一覧取得
    - publish: 投稿を公開
    - draft: 投稿を下書きに戻す
    """
    queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'updated_at', 'published_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """アクションに応じてシリアライザーを切り替え"""
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def get_queryset(self):
        """
        クエリセットのフィルタリング
        - 一般ユーザー: 公開済み投稿のみ
        - 認証済みユーザー: 自分の投稿は全て表示
        """
        queryset = super().get_queryset()

        # 認証済みユーザーの場合、自分の投稿も含める
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        else:
            # 未認証の場合は公開済みのみ
            queryset = queryset.filter(status='published')

        # カテゴリフィルター
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)

        # タグフィルター
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset.distinct()

    @extend_schema(
        description='自分の投稿一覧を取得',
        tags=['Blog Posts']
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        """認証済みユーザーの投稿一覧を取得"""
        queryset = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='投稿を公開する',
        tags=['Blog Posts']
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAuthorOrReadOnly])
    def publish(self, request, pk=None):
        """投稿を公開する"""
        post = self.get_object()
        post.status = 'published'
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @extend_schema(
        description='投稿を下書きに戻す',
        tags=['Blog Posts']
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAuthorOrReadOnly])
    def draft(self, request, pk=None):
        """投稿を下書きに戻す"""
        post = self.get_object()
        post.status = 'draft'
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='カテゴリ一覧を取得', tags=['Categories']),
    retrieve=extend_schema(description='カテゴリ詳細を取得', tags=['Categories']),
    create=extend_schema(description='カテゴリを作成', tags=['Categories']),
    update=extend_schema(description='カテゴリを更新', tags=['Categories']),
    partial_update=extend_schema(description='カテゴリを部分更新', tags=['Categories']),
    destroy=extend_schema(description='カテゴリを削除', tags=['Categories']),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """
    カテゴリのCRUD操作を提供するViewSet
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


@extend_schema_view(
    list=extend_schema(description='タグ一覧を取得', tags=['Tags']),
    retrieve=extend_schema(description='タグ詳細を取得', tags=['Tags']),
    create=extend_schema(description='タグを作成', tags=['Tags']),
    update=extend_schema(description='タグを更新', tags=['Tags']),
    partial_update=extend_schema(description='タグを部分更新', tags=['Tags']),
    destroy=extend_schema(description='タグを削除', tags=['Tags']),
)
class TagViewSet(viewsets.ModelViewSet):
    """
    タグのCRUD操作を提供するViewSet
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
