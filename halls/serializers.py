from rest_framework import serializers
from decimal import Decimal
from .models import Venue, Hall, HallImage, Amenity, CateringOption


# =====================================================
#                     AMENITY
# =====================================================
class AmenitySerializer(serializers.ModelSerializer):
    """Serializer for hall amenities (features like WiFi, parking, etc.)."""
    class Meta:
        model = Amenity
        fields = '__all__'


# =====================================================
#                     HALL IMAGE
# =====================================================
class HallImageSerializer(serializers.ModelSerializer):
    """Serializer for hall images."""
    class Meta:
        model = HallImage
        fields = ['id', 'hall', 'image', 'caption', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


# =====================================================
#                     HALL
# =====================================================
class HallSerializer(serializers.ModelSerializer):
   
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    images = HallImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    amenities = AmenitySerializer(many=True, read_only=True)
    price_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = Hall
        fields = [
            'id', 'venue', 'venue_name', 'name', 'description',
            'capacity', 'pricing_type', 'price_per_hour', 'price_per_day',
            'created_at', 'average_rating', 'images', 'amenities', 'is_featured', 'discount_percent', 'price_after_discount'
        ]
        read_only_fields = [
            'id', 'created_at', 'venue_name', 'average_rating', 'images', 'amenities'
        ]

    def get_average_rating(self, obj):
        """Calculate the average rating for the hall."""
        reviews = getattr(obj, 'reviews', None)
        if not reviews or not reviews.exists():
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 2)
    

    def get_price_after_discount(self, obj):
        return obj.get_price_after_discount()


# =====================================================
#                     VENUE
# =====================================================
class VenueSerializer(serializers.ModelSerializer):
    
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    halls = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = [
            'id', 'owner', 'owner_name', 'name', 'description',
            'address', 'city', 'latitude', 'longitude',
            'created_at', 'halls'
        ]
        read_only_fields = ['id', 'created_at', 'owner', 'owner_name', 'halls']

    def get_halls(self, obj):
        """Return all halls related to this venue."""
        halls = obj.halls.all()
        return HallSerializer(halls, many=True, context=self.context).data


# =====================================================
#                     CateringOption
# =====================================================

class CateringOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringOption
        fields = '__all__'