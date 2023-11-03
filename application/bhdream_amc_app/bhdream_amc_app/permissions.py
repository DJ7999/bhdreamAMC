from rest_framework import permissions

class IsEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an employee (is_employee=True)
        return request.user.is_authenticated and request.user.is_employee