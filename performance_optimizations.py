# Performance optimizations for Django views
from django.core.cache import cache
from django.db.models import Prefetch
from functools import wraps
import time

def cache_result(timeout=300):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

def optimize_queryset(queryset):
    """Optimize queryset with select_related and prefetch_related"""
    return queryset.select_related().prefetch_related()

def get_optimized_venues():
    """Optimized venues query"""
    from halls.models import Venue
    return Venue.objects.select_related('owner').prefetch_related(
        'halls__images',
        'halls__amenities'
    ).filter(is_active=True)

def get_optimized_services():
    """Optimized services query"""
    from services.models import Service
    return Service.objects.select_related('provider').prefetch_related(
        'plans',
        'payment_methods',
        'extra_services'
    ).filter(is_active=True)

def get_optimized_bookings(user):
    """Optimized bookings query"""
    from bookings.models import Booking
    return Booking.objects.select_related(
        'user', 'venue', 'venue__owner'
    ).prefetch_related(
        'service_bookings__service',
        'payments'
    ).filter(user=user)

# Database connection optimization
def optimize_db_connections():
    """Optimize database connections"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA mmap_size=268435456")  # 256MB

# Memory optimization
def clear_unused_cache():
    """Clear unused cache entries"""
    cache.clear()

# Query optimization helpers
def get_user_stats_optimized(user):
    """Optimized user stats calculation"""
    from django.db.models import Count, Sum
    
    if user.role == 'OWNER':
        return {
            'total_venues': user.venues.count(),
            'total_bookings': user.venues.aggregate(
                total=Count('bookings')
            )['total'] or 0,
        }
    elif user.role == 'SERVICE':
        return {
            'total_services': user.provided_services.count(),
            'total_bookings': user.provided_services.aggregate(
                total=Count('service_bookings__booking')
            )['total'] or 0,
        }
    elif user.role == 'USER':
        return {
            'total_bookings': user.bookings.count()
        }
    return {}
