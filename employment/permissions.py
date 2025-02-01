from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee)


class IsEmployer(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employer)
    

class IsEmployerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return False
            if not request.user.is_employer:
                return False
            return True
        
        return True


class IsCompanyManager(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_employer and request.user.employer == obj.manager
