from django.contrib import admin
from .models import Venue, Hall, HallImage, Amenity, CateringOption


# 🖼️ Hall Images Inline
class HallImageInline(admin.TabularInline):
    model = HallImage
    extra = 1


# 🏛️ Hall Admin
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'capacity', 'pricing_type', 'is_active')
    list_filter = ('pricing_type', 'is_active')
    search_fields = ('name', 'venue__name')
    inlines = [HallImageInline]


# 🏠 Venue Admin
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'created_at')
    search_fields = ('name', 'owner__username', 'city')
    list_filter = ('city',)


# 🍴 Catering Options Admin
@admin.register(CateringOption)
class CateringOptionAdmin(admin.ModelAdmin):
    list_display = ('hall', 'name', 'price_per_person', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('hall__name', 'name')


# 🏢 Amenity Admin
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


# ✅ Admin Branding
admin.site.site_header = "Wedly Management Admin"
admin.site.site_title = "Wedly Admin Panel"
admin.site.index_title = "Dashboard Overview"
