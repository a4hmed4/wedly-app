from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from .models import Service, ServicePlan, ServicePaymentMethod, ExtraService
from .serializers import (
    ServiceSerializer,
    ServicePlanSerializer,
    ServicePaymentMethodSerializer,
    ExtraServiceSerializer
)
from accounts.permissions import IsServiceProvider, IsAdmin

User = get_user_model()


# ======================================================
#                  SERVICE VIEWSET
# ======================================================


class ServiceViewSet(viewsets.ModelViewSet):
   
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer

    def get_permissions(self):
       
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'mine']:
            permission_classes = [permissions.IsAuthenticated, (IsServiceProvider | IsAdmin)]
        else:
            permission_classes = [permissions.AllowAny]
        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        """
         إنشاء خدمة جديدة بواسطة مقدم خدمة فقط
        """
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in.")
        if user.role != 'SERVICE' and not user.is_superuser:
            raise PermissionDenied("Only service providers can create services.")
        serializer.save(provider=user)

    def perform_update(self, serializer):
        """
         تعديل خدمة خاصة بمقدم الخدمة نفسه
        """
        instance = self.get_object()
        user = self.request.user
        if instance.provider != user and not user.is_superuser:
            raise PermissionDenied("You can only update your own services.")
        serializer.save()

    def perform_destroy(self, instance):
        """
         حذف الخدمة الخاصة بمقدم الخدمة نفسه
        """
        user = self.request.user
        if instance.provider != user and not user.is_superuser:
            raise PermissionDenied("You can only delete your own services.")
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        """
         عرض جميع الخدمات الخاصة بمقدم الخدمة الحالي
        /api/services/mine/
        """
        services = self.queryset.filter(provider=request.user)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)


# ======================================================
#                  SERVICE PLAN VIEWSET
# ======================================================
class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.all()
    serializer_class = ServicePlanSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, (IsServiceProvider | IsAdmin)]
        else:
            permission_classes = [permissions.AllowAny]
        return [perm() for perm in permission_classes]


# ======================================================
#             SERVICE PAYMENT METHOD VIEWSET
# ======================================================
class ServicePaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = ServicePaymentMethod.objects.all()
    serializer_class = ServicePaymentMethodSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, (IsServiceProvider | IsAdmin)]
        else:
            permission_classes = [permissions.AllowAny]
        return [perm() for perm in permission_classes]


# ======================================================
#                  EXTRA SERVICE VIEWSET
# ======================================================
class ExtraServiceViewSet(viewsets.ModelViewSet):
    queryset = ExtraService.objects.all()
    serializer_class = ExtraServiceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, (IsServiceProvider | IsAdmin)]
        else:
            permission_classes = [permissions.AllowAny]
        return [perm() for perm in permission_classes]
