from rest_framework import permissions

class IsServiceOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj.booking.user, 'id', None) == request.user.id
