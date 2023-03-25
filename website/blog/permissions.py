from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Читать могут все, вносить изменения только автор.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Читать могут все, вносить изменения только персонал сайта.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
