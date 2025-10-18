# 🎉 النظام المحسن للحجز المتكامل - دليل شامل

## 📋 المميزات الجديدة المضافة

### ✅ 1. خطط الخدمات وأسعارها
- كل مقدم خدمة يحدد خطط متعددة لخدمته
- أسعار مختلفة لكل خطة
- إمكانية تحديد الخطة الشائعة (Popular)

### ✅ 2. وسائل الدفع وروابط الدفع
- مقدمي الخدمات يحددون وسائل الدفع المتاحة
- روابط الدفع المباشرة (PayPal, Stripe, إلخ)
- أرقام الحسابات والمحافظ الرقمية

### ✅ 3. ربط مقدمي الخدمات بالقاعات
- **عمل حر**: يعمل مع أي قاعة
- **مقيد بقاعة**: يعمل مع قاعات محددة
- إمكانية إضافة قاعات مخصصة غير موجودة في النظام

### ✅ 4. أوقات التسليم
- كل خدمة لها وقت تسليم محدد
- حساب تلقائي لوقت التسليم بعد تأكيد الحجز

### ✅ 5. عرض مقدمي الخدمات لأصحاب القاعات
- أصحاب القاعات يرون مقدمي الخدمات المرتبطين بقاعاتهم
- إمكانية الموافقة أو رفض مقدمي الخدمات

### ✅ 6. حجز منفصل للخدمات
- حجز القاعة أولاً
- إضافة الخدمات لاحقاً
- إشعار تلقائي لصاحب القاعة عند إضافة خدمة

### ✅ 7. إرسال نسخ على الجيميل
- إشعارات تلقائية للحجوزات
- نسخ من الفواتير
- تأكيدات الخدمات

## 🏗️ النماذج الجديدة

### 1. ServicePlan (خطط الخدمات)
```python
class ServicePlan(models.Model):
    service = models.ForeignKey(ExtraService, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.PositiveIntegerField(default=1)
    is_popular = models.BooleanField(default=False)
    # ... المزيد من الحقول
```

### 2. ServicePaymentMethod (وسائل الدفع)
```python
class ServicePaymentMethod(models.Model):
    service = models.ForeignKey(ExtraService, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_link = models.URLField(blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    # ... المزيد من الحقول
```

### 3. VenueServiceProvider (ربط مقدمي الخدمات بالقاعات)
```python
class VenueServiceProvider(models.Model):
    venue = models.ForeignKey('halls.Venue', on_delete=models.CASCADE)
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    is_approved = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    # ... المزيد من الحقول
```

### 4. ServiceBooking (حجز الخدمات المنفصل)
```python
class ServiceBooking(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    service = models.ForeignKey('services.ExtraService', on_delete=models.CASCADE)
    service_plan = models.ForeignKey('services.ServicePlan', on_delete=models.CASCADE)
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    delivery_date = models.DateTimeField(null=True, blank=True)
    # ... المزيد من الحقول
```

### 5. EmailNotification (إشعارات البريد الإلكتروني)
```python
class EmailNotification(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    # ... المزيد من الحقول
```

## 🔄 تدفق العمل المحسن

### 1. إعداد مقدم الخدمة
```http
# 1. إنشاء خدمة
POST /api/enhanced-extra-services/
{
    "name": "تصوير زفاف احترافي",
    "service_type": "PHOTOGRAPHY",
    "work_type": "FREELANCE",  # أو "VENUE_BASED"
    "delivery_time_hours": 48,
    "associated_venues": [1, 2]  # إذا كان VENUE_BASED
}

# 2. إضافة خطط للخدمة
POST /api/service-plans/
{
    "service": 1,
    "name": "حزمة أساسية",
    "price": 1500.00,
    "duration_hours": 6,
    "includes": "تصوير كامل + 100 صورة"
}

# 3. إضافة وسائل الدفع
POST /api/service-payment-methods/
{
    "service": 1,
    "method": "PAYPAL",
    "payment_link": "https://paypal.me/photographer",
    "account_name": "مصور محترف"
}
```

### 2. حجز القاعة أولاً
```http
POST /api/bookings/
{
    "hall": 1,
    "date": "2024-06-15",
    "start_time": "18:00",
    "end_time": "23:00",
    "total_guests": 150,
    "catering": 1
}
```

### 3. إضافة الخدمات لاحقاً
```http
POST /api/service-bookings/
{
    "booking": 1,
    "service": 1,
    "service_plan": 1,
    "notes": "تصوير زفاف في القاعة"
}
```

### 4. تأكيد الخدمة من مقدم الخدمة
```http
POST /api/service-bookings/1/confirm/
```

## 📊 API Endpoints الجديدة

### خطط الخدمات
```http
GET /api/service-plans/                    # جميع الخطط
GET /api/service-plans/?service=1          # خطط خدمة معينة
GET /api/service-plans/mine/               # خطط المستخدم الحالي
POST /api/service-plans/                   # إضافة خطة جديدة
```

### وسائل الدفع
```http
GET /api/service-payment-methods/          # جميع وسائل الدفع
GET /api/service-payment-methods/?service=1 # وسائل دفع خدمة معينة
GET /api/service-payment-methods/mine/     # وسائل دفع المستخدم الحالي
POST /api/service-payment-methods/         # إضافة وسيلة دفع جديدة
```

### ربط مقدمي الخدمات بالقاعات
```http
GET /api/venue-service-providers/          # جميع الروابط
GET /api/venue-service-providers/?venue=1  # مقدمي خدمة قاعة معينة
GET /api/venue-service-providers/mine/     # مقدمي خدمة المستخدم الحالي
POST /api/venue-service-providers/1/approve/ # موافقة على مقدم خدمة
```

### حجز الخدمات المنفصل
```http
GET /api/service-bookings/                 # جميع حجوزات الخدمات
GET /api/service-bookings/?booking=1       # خدمات حجز معين
GET /api/service-bookings/mine/            # خدمات المستخدم الحالي
POST /api/service-bookings/1/confirm/      # تأكيد الخدمة
```

### الإشعارات
```http
GET /api/email-notifications/              # جميع الإشعارات
GET /api/email-notifications/mine/        # إشعارات المستخدم الحالي
POST /api/email-notifications/1/resend/   # إعادة إرسال إشعار
```

## 💰 نظام توزيع الأرباح المحسن

### للمالك (صاحب القاعة):
- يحصل على 100% من مبلغ القاعة
- يحصل على 100% من مبلغ الكاترينج
- عمولة من مقدمي الخدمات المرتبطين بقاعته (حسب الاتفاق)

### لمقدمي الخدمات:
- يحصل على المبلغ المتفق عليه مع صاحب القاعة
- يمكن تحديد عمولة مختلفة لكل قاعة

### مثال على التوزيع المحسن:
```
حجز بقيمة 15,000 جنيه:
├── قاعة: 8,000 جنيه (للمالك)
├── كاترينج: 3,000 جنيه (للمالك)
├── تصوير: 2,500 جنيه (لمقدم الخدمة: 2,375 جنيه + 125 جنيه عمولة للمالك)
├── ديكور: 1,200 جنيه (لمقدم الخدمة: 1,140 جنيه + 60 جنيه عمولة للمالك)
└── موسيقى: 300 جنيه (لمقدم الخدمة: 285 جنيه + 15 جنيه عمولة للمالك)
```

## 📧 نظام الإشعارات التلقائية

### 1. عند حجز القاعة:
- إيميل تأكيد للعميل
- إيميل إشعار لصاحب القاعة

### 2. عند إضافة خدمة:
- إيميل إشعار لصاحب القاعة
- إيميل تأكيد للعميل عند موافقة مقدم الخدمة

### 3. عند تأكيد الخدمة:
- إيميل تأكيد للعميل مع تفاصيل التسليم
- إيميل إشعار لصاحب القاعة

### 4. عند إنشاء الفاتورة:
- إيميل الفاتورة للعميل
- إيميل نسخة لصاحب القاعة

## 🎯 سيناريوهات الاستخدام

### السيناريو 1: مقدم خدمة حر
1. يسجل كمقدم خدمة
2. يضيف خدماته مع الخطط والأسعار
3. يحدد وسائل الدفع
4. يختار "عمل حر" ليعمل مع أي قاعة
5. العملاء يحجزون خدماته مباشرة

### السيناريو 2: مقدم خدمة مقيد بقاعة
1. يسجل كمقدم خدمة
2. يطلب الانضمام لقاعة معينة
3. صاحب القاعة يوافق عليه
4. يضيف خدماته مع الأسعار
5. العملاء يحجزون من خلال القاعة

### السيناريو 3: حجز متدرج
1. العميل يحجز القاعة أولاً
2. يضيف الخدمات لاحقاً
3. مقدمي الخدمات يتلقون إشعارات
4. يؤكدون الخدمات
5. يتم إرسال إشعارات للجميع

## 🔧 إعداد النظام

### 1. تشغيل Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. إعداد إيميلات النظام
```python
# في settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'WeddingApp <your-email@gmail.com>'
```

### 3. إنشاء مستخدمين تجريبيين
```python
# في Django shell
from accounts.models import User
from services.models import ExtraService, ServicePlan, ServicePaymentMethod

# مقدم خدمة تصوير
photographer = User.objects.create_user(
    username='photographer',
    email='photo@example.com',
    role='SERVICE',
    business_type='PHOTOGRAPHY'
)

# إنشاء خدمة تصوير
service = ExtraService.objects.create(
    provider=photographer,
    name='تصوير زفاف احترافي',
    service_type='PHOTOGRAPHY',
    work_type='FREELANCE',
    delivery_time_hours=48
)

# إضافة خطة للخدمة
plan = ServicePlan.objects.create(
    service=service,
    name='حزمة كاملة',
    price=2500.00,
    duration_hours=8,
    is_popular=True
)

# إضافة وسيلة دفع
payment_method = ServicePaymentMethod.objects.create(
    service=service,
    method='PAYPAL',
    payment_link='https://paypal.me/photographer',
    account_name='مصور محترف'
)
```

## 📱 واجهة المستخدم المقترحة

### 1. لوحة تحكم مقدم الخدمة:
- إدارة الخدمات والخطط
- إدارة وسائل الدفع
- طلبات الحجز الجديدة
- تقارير الأرباح

### 2. لوحة تحكم صاحب القاعة:
- إدارة القاعات
- مقدمي الخدمات المرتبطين
- الحجوزات والخدمات
- التقارير المالية

### 3. لوحة تحكم العميل:
- تصفح القاعات والخدمات
- حجز القاعة
- إضافة الخدمات
- متابعة الحجوزات

## 🎉 الخلاصة

النظام المحسن يوفر:

- ✅ **مرونة كاملة**: مقدمي الخدمات يحددون خططهم وأسعارهم
- ✅ **ربط ذكي**: ربط مقدمي الخدمات بالقاعات أو العمل الحر
- ✅ **حجز متدرج**: حجز القاعة أولاً ثم إضافة الخدمات
- ✅ **إشعارات تلقائية**: إيميلات للجميع عند كل خطوة
- ✅ **توزيع عادل**: نظام عمولات مرن ومتدرج
- ✅ **إدارة شاملة**: لوحات تحكم لكل نوع مستخدم

هذا النظام يوفر حلاً متكاملاً ومرناً لإدارة حجوزات القاعات مع الخدمات الإضافية! 🎉
