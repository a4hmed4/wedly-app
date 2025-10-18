from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from decimal import Decimal
from geopy.distance import geodesic

from accounts.permissions import IsAdmin, IsVenueOwner
from .models import Venue, Hall, HallImage, Amenity, CateringOption
from .serializers import (
    VenueSerializer,
    HallSerializer,
    HallImageSerializer,
    AmenitySerializer,
    CateringOptionSerializer
)
from .permissions import IsOwnerOrReadOnly
from accounts.permissions import IsVenueOwner
from accounts.permissions import IsVenueOwner
# ======================================================
#                     VENUE VIEWSET
# ======================================================

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all().select_related('owner')
    serializer_class = VenueSerializer

    def get_permissions(self):
        """
        تحديد الصلاحيات حسب نوع العملية.
        """
        if self.action in ['create_venue', 'update_venue', 'delete_venue']:
            permission_classes = [permissions.IsAuthenticated, IsVenueOwner]
        else:
            permission_classes = [permissions.AllowAny]
        return [perm() for perm in permission_classes]

    # ----------------------------------------------
    # إنشاء Venue جديدة
    # ----------------------------------------------
    @action(detail=False, methods=['post'], url_path='create')
    def create_venue(self, request):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a venue.")
        if user.role != 'OWNER' and not user.is_superuser:
            raise PermissionDenied("Only venue owners can create venues.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ----------------------------------------------
    #  تعديل Venue
    # ----------------------------------------------
    @action(detail=True, methods=['put', 'patch'], url_path='update')
    def update_venue(self, request, pk=None):
        venue = self.get_object()
        if venue.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied("You are not allowed to update this venue.")

        serializer = self.get_serializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ----------------------------------------------
    #  حذف Venue
    # ----------------------------------------------
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_venue(self, request, pk=None):
        venue = self.get_object()
        if venue.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied("You are not allowed to delete this venue.")
        venue.delete()
        return Response({'detail': 'Venue deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    # ----------------------------------------------
    # عرض الأماكن الخاصة بالمستخدم الحالي
    # ----------------------------------------------
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        venues = self.queryset.filter(owner=request.user)
        return Response(self.get_serializer(venues, many=True).data)

    # ----------------------------------------------
    #  عرض الأماكن القريبة
    # ----------------------------------------------
    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby(self, request):
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        radius = float(request.query_params.get('radius', 10))  # كم

        if not lat or not lon:
            return Response(
                {"error": "latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_location = (float(lat), float(lon))
        nearby_venues = []

        for venue in self.queryset:
            if venue.latitude and venue.longitude:
                distance = geodesic(user_location, (venue.latitude, venue.longitude)).km
                if distance <= radius:
                    nearby_venues.append(venue)

        serializer = self.get_serializer(nearby_venues, many=True)
        return Response(serializer.data)


# ======================================================
#                     HALL VIEWSET
# ======================================================
class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all().select_related('venue').prefetch_related('images')
    serializer_class = HallSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """المالك فقط يضيف قاعة لمكانه"""
        user = self.request.user
        venue = serializer.validated_data.get('venue')

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in.")

        if venue.owner != user and not user.is_superuser:
            raise PermissionDenied("You can only add halls to your own venues.")
        serializer.save()

    def get_queryset(self):
        """لو فيه mine في البارامتر، يعرض قاعات المستخدم فقط"""
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.query_params.get('mine'):
            qs = qs.filter(venue__owner=self.request.user)
        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_images(self, request, pk=None):
        """رفع صور القاعة"""
        hall = self.get_object()
        if hall.venue.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied("You can only upload images to your own halls.")

        files = request.FILES.getlist('images')
        created = [
            HallImageSerializer(HallImage.objects.create(hall=hall, image=f)).data
            for f in files
        ]
        return Response({'created': created}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def top(self, request):
        """أفضل القاعات"""
        limit = int(request.query_params.get('limit', 10))
        city = request.query_params.get('city')
        capacity = request.query_params.get('capacity')

        qs = self.get_queryset().filter(is_active=True)
        if city:
            qs = qs.filter(venue__city__icontains=city)
        if capacity:
            qs = qs.filter(capacity__gte=int(capacity))

        qs = qs.order_by('-average_rating', '-reviews_count')[:limit]
        serializer = self.get_serializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """بحث متقدم عن القاعات"""
        city = request.query_params.get('city')
        capacity_min = request.query_params.get('capacity_min')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        qs = self.queryset

        if city:
            qs = qs.filter(venue__city__icontains=city)
        if capacity_min:
            qs = qs.filter(capacity__gte=int(capacity_min))

        if price_min or price_max:
            pmin = Decimal(price_min) if price_min else None
            pmax = Decimal(price_max) if price_max else None
            price_q = Q()
            if pmin and pmax:
                price_q = (
                    Q(price_per_day__gte=pmin, price_per_day__lte=pmax) |
                    Q(price_per_hour__gte=pmin, price_per_hour__lte=pmax)
                )
            elif pmin:
                price_q = Q(price_per_day__gte=pmin) | Q(price_per_hour__gte=pmin)
            elif pmax:
                price_q = Q(price_per_day__lte=pmax) | Q(price_per_hour__lte=pmax)
            qs = qs.filter(price_q)

        serializer = HallSerializer(qs.distinct(), many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """القاعات المميزة"""
        qs = self.get_queryset().filter(is_featured=True, is_active=True)
        serializer = self.get_serializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


# ======================================================
#                   AMENITY VIEWSET
# ======================================================
class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]


# ======================================================
#                   CATERING OPTION VIEWSET
# ======================================================
class CateringOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CateringOption.objects.all()
    serializer_class = CateringOptionSerializer
    permission_classes = [permissions.AllowAny]
