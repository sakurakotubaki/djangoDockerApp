from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, Category, Tag


class UserSerializer(serializers.ModelSerializer):
    """ユーザーシリアライザー(読み取り専用)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields


class TagSerializer(serializers.ModelSerializer):
    """タグシリアライザー"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_slug(self, value):
        # スラッグのバリデーション
        if not value.replace('-', '').isalnum():
            raise serializers.ValidationError('スラッグは英数字とハイフンのみ使用できます')
        return value.lower()


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリシリアライザー"""
    posts_count = serializers.IntegerField(
        source='posts.count',
        read_only=True
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_slug(self, value):
        if not value.replace('-', '').isalnum():
            raise serializers.ValidationError('スラッグは英数字とハイフンのみ使用できます')
        return value.lower()


class BlogPostListSerializer(serializers.ModelSerializer):
    """ブログ投稿リストシリアライザー(一覧表示用・軽量版)"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'excerpt', 'author', 'status',
            'category', 'tags', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_excerpt(self, obj):
        """本文の最初の200文字を抜粋"""
        return obj.body[:200] + '...' if len(obj.body) > 200 else obj.body


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """ブログ投稿詳細シリアライザー(詳細表示・作成・更新用)"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'body', 'author', 'status',
            'category', 'category_id', 'tags', 'tag_ids',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'published_at']

    def validate_status(self, value):
        """ステータスのバリデーション"""
        if value not in ['draft', 'published']:
            raise serializers.ValidationError('無効なステータスです')
        return value

    def create(self, validated_data):
        """投稿作成時に著者を自動設定"""
        validated_data['author'] = self.context['request'].user
        tags = validated_data.pop('tags', [])
        post = BlogPost.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        """投稿更新"""
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance
