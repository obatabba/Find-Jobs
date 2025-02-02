from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from employment.models import Company


class IsEmployee(BasePermission):
    """Checks if the user is authenticated and is an employee."""

    def has_permission(self, request, view):
        return getattr(request.user, 'is_employee', False)


class IsEmployer(BasePermission):
    """Checks if the user is authenticated and is an employer."""

    def has_permission(self, request, view):
        return getattr(request.user, 'is_employer', False)
    

class IsEmployerOrReadOnly(BasePermission):
    """Allows only employers to create companies, update and delete only their companies. Read access is open to everyone."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return IsEmployer().has_permission(request, view)        
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and
            request.user.is_employer and
            request.user.employer == obj.manager
        )


class IsTheManager(BasePermission):
    """Allows only company managers to create, update, or delete jobs. Read access is open to everyone."""
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            if not IsEmployer().has_permission(request, view):
                return False

            company_id = view.kwargs.get('company_pk')
            if not company_id:
                return False

            company = get_object_or_404(Company, id=company_id)
            return request.user.employer == company.manager

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and 
            request.user.is_employer and 
            request.user.employer == obj.company.manager
        )
