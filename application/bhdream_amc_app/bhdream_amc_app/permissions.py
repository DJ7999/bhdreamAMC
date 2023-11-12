# permissions.py
from rest_framework import permissions
from django.contrib.auth.models import User

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=request.user.username)
            return user.is_authenticated and user.is_superuser
        except User.DoesNotExist:
            return False

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=request.user.username)
            return user.is_authenticated and user.is_staff
        except User.DoesNotExist:
            return False

class IsNormalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=request.user.username)
            return user.is_authenticated and not user.is_staff and not user.is_superuser
        except User.DoesNotExist:
            return False
