from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Читать могут все, вносить изменения только автор.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user
        )


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Читать могут все, вносить изменения только персонал сайта.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff
        )
