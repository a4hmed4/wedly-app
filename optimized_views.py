# Optimized views for better performance
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Prefetch, Count, Sum
from .performance_optimizations import cache_result, get_optimized_venues, get_optimized_services

class OptimizedVenueViewSet(viewsets.ModelViewSet):
    """Optimized Venue ViewSet with caching and query optimization"""
    
    def get_queryset(self):
        """Optimized queryset with select_related and prefetch_related"""
        return get_optimized_venues()
    
    @cache_result(timeout=300)  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        """Cached list view"""
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Optimized retrieve with caching"""
        cache_key = f"venue_{kwargs.get('pk')}"
        venue_data = cache.get(cache_key)
        
        if venue_data is None:
            venue = self.get_object()
            serializer = self.get_serializer(venue)
            venue_data = serializer.data
            cache.set(cache_key, venue_data, 600)  # Cache for 10 minutes
        
        return Response(venue_data)

class OptimizedServiceViewSet(viewsets.ModelViewSet):
    """Optimized Service ViewSet with caching"""
    
    def get_queryset(self):
        """Optimized queryset"""
        return get_optimized_services()
    
    @cache_result(timeout=300)
    def list(self, request, *args, **kwargs):
        """Cached list view"""
        return super().list(request, *args, **kwargs)
    
    def get_serializer_context(self):
        """Add request context for serializers"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class OptimizedBookingViewSet(viewsets.ModelViewSet):
    """Optimized Booking ViewSet"""
    
    def get_queryset(self):
        """Optimized queryset for bookings"""
        from bookings.models import Booking
        return Booking.objects.select_related(
            'user', 'venue', 'venue__owner'
        ).prefetch_related(
            'service_bookings__service',
            'payments'
        ).filter(user=self.request.user)
    
    @cache_result(timeout=180)  # Cache for 3 minutes
    def list(self, request, *args, **kwargs):
        """Cached bookings list"""
        return super().list(request, *args, **kwargs)

# Optimized dashboard views
class OptimizedDashboardView:
    """Base class for optimized dashboard views"""
    
    @staticmethod
    def get_user_stats_cached(user):
        """Get user stats with caching"""
        cache_key = f"user_stats_{user.id}_{user.role}"
        stats = cache.get(cache_key)
        
        if stats is None:
            from .performance_optimizations import get_user_stats_optimized
            stats = get_user_stats_optimized(user)
            cache.set(cache_key, stats, 300)  # Cache for 5 minutes
        
        return stats
    
    @staticmethod
    def clear_user_cache(user):
        """Clear user-specific cache"""
        cache.delete(f"user_stats_{user.id}_{user.role}")
        cache.delete_pattern(f"*_user_{user.id}_*")

# Database query optimization helpers
def optimize_venue_queries():
    """Optimize venue-related queries"""
    from halls.models import Venue, Hall
    return Venue.objects.select_related('owner').prefetch_related(
        Prefetch('halls', queryset=Hall.objects.select_related('venue').prefetch_related('images'))
    )

def optimize_service_queries():
    """Optimize service-related queries"""
    from services.models import Service, ServicePlan, ServicePaymentMethod
    return Service.objects.select_related('provider').prefetch_related(
        Prefetch('plans', queryset=ServicePlan.objects.all()),
        Prefetch('payment_methods', queryset=ServicePaymentMethod.objects.filter(is_active=True))
    )

def optimize_booking_queries(user):
    """Optimize booking queries for specific user"""
    from bookings.models import Booking
    return Booking.objects.select_related(
        'user', 'venue', 'venue__owner'
    ).prefetch_related(
        'service_bookings__service',
        'payments'
    ).filter(user=user).order_by('-created_at')
