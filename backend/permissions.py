from rest_framework.permissions import BasePermission


class IsUserAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        if str(request.user.id) != user_id:
            return False
        return True
