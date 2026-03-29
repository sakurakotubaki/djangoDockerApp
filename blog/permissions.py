from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    カスタム権限: 著者のみ編集・削除可能
    読み取りは認証済みユーザー全員に許可
    """

    def has_object_permission(self, request, view, obj):
        # 読み取り操作(GET, HEAD, OPTIONS)は常に許可
        if request.method in permissions.SAFE_METHODS:
            return True

        # 書き込み操作は著者のみ許可
        return obj.author == request.user
