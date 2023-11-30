# permissions.py
from rest_framework import permissions
from django.contrib.auth.models import User

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            is_superuser=request.decoded_token.get('is_superuser')
            return is_superuser
        except User.DoesNotExist:
            return False

class IsStaffUser(IsAdminUser):
    def has_permission(self, request, view):
        try:
           
            is_staff=request.decoded_token.get('is_staff')
            return is_staff or super().has_permission(request, view)
        except User.DoesNotExist:
            return False

