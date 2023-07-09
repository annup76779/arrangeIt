from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class IsOrgAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # Check if the authenticated user has the required role
        required_roles = 1  # Update with your desired roles
        user = request.user
        if user.role == required_roles:
            return True
        return False


class IsMemberAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # Check if the authenticated user has the required role
        required_roles = 2  # Update with your desired roles
        user = request.user
        if user.role == required_roles:
            return True
        return False
