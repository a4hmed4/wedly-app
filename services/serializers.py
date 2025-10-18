from rest_framework import serializers
from .models import Service, ServicePlan, ServicePaymentMethod, ExtraService


class ServicePaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePaymentMethod
        fields = '__all__'


class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    plans = ServicePlanSerializer(many=True, read_only=True)
    payment_methods = ServicePaymentMethodSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'


""" class ServiceBookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True
    )

    class Meta:
        model = ServiceBooking
        fields = ['id', 'booking', 'service', 'service_id', 'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['total_price', 'created_at']
 """



class ExtraServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta: 
        model = ExtraService
        fields = [
            'id', 'service', 'service_name', 'name', 'description',
            'price', 'is_available', 'created_at'
        ]