from rest_framework.permissions import BasePermission


class IsBookingOwner(BasePermission):
    """Only the user who created the booking can view or modify it."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
