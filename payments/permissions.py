from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        user = getattr(obj, 'user', None)
        return request.method in SAFE_METHODS or (user == request.user)
