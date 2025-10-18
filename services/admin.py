from django.contrib import admin
from .models import Service, ServicePlan, ServicePaymentMethod
#from bookings.models import ServiceBooking



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('service_type', 'name')


@admin.register(ServicePlan)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ('service', 'name', 'price', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'service__name')


""" @admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'booking', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('service__name', 'booking__venue__name')

 """
@admin.register(ServicePaymentMethod)
class ServicePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('service', 'method', 'account_name', 'is_active')
    list_filter = ('method', 'is_active')
