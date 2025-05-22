# permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerBarberOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow all users to read
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only allow owner (barber user) to modify
        return obj.barber.user == request.user
