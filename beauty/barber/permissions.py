# permissions.py
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS

class IsOwnerBarberOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow all users to read
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only allow owner (barber user) to modify
        return obj.barber.user == request.user


class IsBarberOwnerOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and (request.user == obj.user or request.user.is_superuser)


class IsSuperUserOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser