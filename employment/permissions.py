from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee)
    

class IsEmployer(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employer)