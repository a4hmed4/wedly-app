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
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

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
        # Set business_type default from user's business_type
        business_type = getattr(user, 'business_type', None)
        serializer.save(provider=user, business_type=business_type or serializer.validated_data.get('business_type'))

    def perform_update(self, serializer):
        """
         تعديل خدمة خاصة بمقدم الخدمة نفسه
        """
        instance = self.get_object()
        user = self.request.user
        if instance.provider != user and not user.is_superuser:
            raise PermissionDenied("You can only update your own services.")
        # Keep existing business_type unless explicitly changed
        if 'business_type' not in serializer.validated_data:
            serializer.validated_data['business_type'] = serializer.instance.business_type
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


# ======================================================
#           PROVIDER STOREFRONT (Profile + Services)
# ======================================================


class ProviderStorefrontView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsServiceProvider]

    def get(self, request):
        user = request.user
        # Provider basic profile
        profile = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': getattr(user, 'bio', ''),
            'address': getattr(user, 'address', ''),
            'profile_image': getattr(user, 'profile_image', None).url if getattr(user, 'profile_image', None) else None,
            'business_type': getattr(user, 'business_type', None),
        }

        # Services + nested plans/payment methods/extra services
        services_qs = Service.objects.filter(provider=user, is_active=True)
        services_data = ServiceSerializer(services_qs, many=True, context={'request': request}).data
        return Response({
            'profile': profile,
            'services': services_data,
        })

    def patch(self, request):
        user = request.user
        updated = {}

        # Update provider profile fields
        profile_fields = ['bio', 'address']
        profile_changes = False
        for f in profile_fields:
            if f in request.data:
                setattr(user, f, request.data.get(f))
                profile_changes = True
        if profile_changes:
            user.save(update_fields=[f for f in profile_fields if f in request.data])
            updated['profile'] = 'updated'

        # Update or create a primary service (if provided)
        service_payload = request.data.get('service')
        if service_payload:
            service_id = service_payload.get('id')
            if service_id:
                service = Service.objects.filter(id=service_id, provider=user).first()
            else:
                service = Service.objects.filter(provider=user).first()
            if not service:
                service = Service(provider=user, name=service_payload.get('name') or f"{user.username}'s Service", price=service_payload.get('price') or 0, service_type=service_payload.get('service_type') or 'PHOTOGRAPHY')
            # Allowed updatable fields
            updatable = ['name', 'description', 'service_type', 'price', 'duration_hours', 'max_capacity', 'is_active']
            for f in updatable:
                if f in service_payload:
                    setattr(service, f, service_payload.get(f))
            service.save()
            updated['service'] = service.id

        return Response({'updated': updated})


class StorefrontSchemaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service_type = request.query_params.get('service_type') or 'PHOTOGRAPHY'
        # Minimal schemas per type
        base = [
            {'field': 'name', 'type': 'string', 'required': True},
            {'field': 'description', 'type': 'text', 'required': False},
            {'field': 'price', 'type': 'number', 'required': True},
            {'field': 'duration_hours', 'type': 'number', 'required': False},
            {'field': 'max_capacity', 'type': 'number', 'required': False},
        ]
        extras_by_type = {
            'PHOTOGRAPHY': [{'field': 'deliverables', 'type': 'list[string]', 'required': False}],
            'MAKEUP': [{'field': 'brands_used', 'type': 'list[string]', 'required': False}],
            'CATERING': [{'field': 'menu_types', 'type': 'list[string]', 'required': False}],
            'MUSIC': [{'field': 'genres', 'type': 'list[string]', 'required': False}],
        }
        schema = base + extras_by_type.get(service_type, [])
        return Response({'service_type': service_type, 'schema': schema})
