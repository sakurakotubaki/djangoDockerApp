from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CategoryViewSet, TagViewSet

# DRF Routerでエンドポイントを自動生成
router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]
