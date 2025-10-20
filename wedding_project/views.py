from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index_view(request):
    """الصفحة الرئيسية لعرض APIs Dashboard"""
    return render(request, 'index.html')

def admin_access_view(request):
    """صفحة الوصول للوحة التحكم الإدارية"""
    return render(request, 'admin_access.html')

def api_info_view(request):
    """معلومات APIs في JSON format"""
    apis = {
        "accounts": {
            "register": {"method": "POST", "url": "/accounts/register/", "description": "تسجيل مستخدم جديد"},
            "login": {"method": "POST", "url": "/accounts/login/", "description": "تسجيل الدخول"},
            "profile": {"method": "GET", "url": "/accounts/profile/", "description": "الملف الشخصي"},
            "dashboard_user": {"method": "GET", "url": "/accounts/dashboard/user/", "description": "لوحة المستخدم"},
            "dashboard_admin": {"method": "GET", "url": "/accounts/dashboard/admin/", "description": "لوحة الإدارة"},
            "dashboard_owner": {"method": "GET", "url": "/accounts/dashboard/owner/", "description": "لوحة المالك"},
            "dashboard_service": {"method": "GET", "url": "/accounts/dashboard/service/", "description": "لوحة مقدم الخدمة"},
        },
        "halls": {
            "list": {"method": "GET", "url": "/halls/", "description": "قائمة القاعات"},
            "featured": {"method": "GET", "url": "/halls/featured/", "description": "القاعات المميزة"},
            "create": {"method": "POST", "url": "/halls/", "description": "إضافة قاعة جديدة"},
        },
        "services": {
            "list": {"method": "GET", "url": "/services/", "description": "قائمة الخدمات"},
            "create": {"method": "POST", "url": "/services/", "description": "إضافة خدمة جديدة"},
            "storefront": {"method": "GET", "url": "/services/storefront/", "description": "واجهة المتجر"},
            "schema": {"method": "GET", "url": "/services/schema/", "description": "مخطط الخدمات"},
        },
        "bookings": {
            "list": {"method": "GET", "url": "/bookings/", "description": "قائمة الحجوزات"},
            "create": {"method": "POST", "url": "/bookings/", "description": "حجز جديد"},
            "my_bookings": {"method": "GET", "url": "/bookings/my-bookings/", "description": "حجوزاتي"},
        },
        "payments": {
            "list": {"method": "GET", "url": "/payments/", "description": "قائمة المدفوعات"},
            "create": {"method": "POST", "url": "/payments/", "description": "دفعة جديدة"},
            "receipt": {"method": "GET", "url": "/payments/receipt/{id}/", "description": "إيصال الدفع"},
        },
        "reviews": {
            "list": {"method": "GET", "url": "/reviews/", "description": "قائمة التقييمات"},
            "create": {"method": "POST", "url": "/reviews/", "description": "تقييم جديد"},
        },
        "notifications": {
            "list": {"method": "GET", "url": "/notifications/", "description": "قائمة الإشعارات"},
            "create": {"method": "POST", "url": "/notifications/", "description": "إشعار جديد"},
            "mark_read": {"method": "PUT", "url": "/notifications/mark-read/{id}/", "description": "تحديد كمقروء"},
        },
        "cloud": {
            "collections": {"method": "GET", "url": "/cloud/collections/", "description": "المجموعات"},
            "firebase_users": {"method": "GET", "url": "/cloud/collections/users/", "description": "مستخدمي Firebase"},
        }
    }
    
    return JsonResponse({
        "message": "WedlyApp APIs Information",
        "version": "1.0.0",
        "base_url": request.build_absolute_uri('/'),
        "admin_url": request.build_absolute_uri('/admin/'),
        "apis": apis
    })
