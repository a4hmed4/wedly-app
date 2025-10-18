from rest_framework import viewsets, permissions
from .serializers import BookingSerializer
from .permissions import IsBookingOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from halls.models import Venue
from services.models import Service
from rest_framework.permissions import IsAuthenticated
from .models import Booking, ServiceBooking, Venue
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class NearbyVenuesServicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # مثال مبسط: إرجاع كل القاعات والخدمات
        # لاحقًا ممكن تستخدم Latitude & Longitude لتحديد القريبة
        venues = Venue.objects.all()
        services = Service.objects.filter(is_active=True)

        venue_data = [
            {"id": v.id, "name": v.name, "address": v.address, "price": v.price_per_day}
            for v in venues
        ]

        service_data = [
            {"id": s.id, "name": s.name, "category": s.get_service_type_display(), "price": s.price}
            for s in services
        ]

        return Response({"venues": venue_data, "services": service_data})




class CreateOrUpdateBookingView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        
        user = request.user
        venue_id = request.data.get("venue_id")
        service_ids = request.data.get("service_ids", [])
        booking_id = request.data.get("booking_id")  # لو عايز تحديث حجز

        if booking_id:
            # تحديث الحجز
            booking = Booking.objects.get(id=booking_id, user=user)
            if venue_id:
                booking.venue_id = venue_id
            booking.calculate_total()
        else:
            # حجز جديد
            if not venue_id:
                return Response({"error": "venue_id required"}, status=400)
            booking = Booking.objects.create(user=user, venue_id=venue_id)
            booking.calculate_total()

        # إضافة الخدمات
        for sid in service_ids:
            service = Service.objects.get(id=sid)
            ServiceBooking.objects.update_or_create(
                booking=booking,
                service=service,
                defaults={"quantity": 1, "price": service.price},
            )

        booking.calculate_total()  # إعادة حساب السعر بعد إضافة الخدمات
        return Response({
            "booking_id": booking.id,
            "total_price": booking.total_price,
        })
