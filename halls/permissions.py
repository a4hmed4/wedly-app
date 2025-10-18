from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        owner = getattr(obj, 'owner', None)
        if owner:
            return owner == request.user

        venue = getattr(obj, 'venue', None)
        if venue:
            return getattr(venue, 'owner', None) == request.user

        return False
