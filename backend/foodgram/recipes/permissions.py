from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user)
