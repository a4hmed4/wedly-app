# 🎉 نظام الحجز المتكامل - دليل الاستخدام

## 📋 نظرة عامة

تم تطوير نظام حجز متكامل للقاعات مع الخدمات الإضافية يتضمن:

- ✅ حجز القاعات مع الخدمات الإضافية
- ✅ حساب المبالغ الإجمالية تلقائياً
- ✅ توزيع الأرباح على مقدمي الخدمات
- ✅ إنشاء فواتير إجمالية
- ✅ تقارير الأرباح للمقدمين
- ✅ نظام التقسيط

## 🏗️ النماذج الجديدة

### 1. ExtraService (الخدمات الإضافية)
```python
# في services/models.py
class ExtraService(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ... المزيد من الحقول
```

### 2. Invoice (الفاتورة الإجمالية)
```python
# في halls/models.py
class Invoice(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # ... المزيد من الحقول
```

### 3. RevenueReport (تقرير الأرباح)
```python
# في halls/models.py
class RevenueReport(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    service_name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # ... المزيد من الحقول
```

## 🔄 تدفق الحجز

### 1. المستخدم يختار القاعة
```http
GET /api/halls/
```

### 2. المستخدم يختار الخدمات الإضافية
```http
GET /api/extra-services/?service_type=PHOTOGRAPHY
```

### 3. إنشاء الحجز
```http
POST /api/bookings/
{
    "hall": 1,
    "date": "2024-06-15",
    "start_time": "18:00",
    "end_time": "23:00",
    "total_guests": 150,
    "catering": 1,
    "extra_services": [1, 2, 3],
    "payment_method": 1,
    "installment_plan": 1
}
```

### 4. النظام يحسب تلقائياً:
- ✅ المبلغ الإجمالي للحجز
- ✅ توزيع الأرباح على مقدمي الخدمات
- ✅ إنشاء الفاتورة الإجمالية
- ✅ تقارير الأرباح لكل مقدم خدمة

## 📊 API Endpoints الجديدة

### الخدمات الإضافية
```http
GET /api/extra-services/                    # جميع الخدمات
GET /api/extra-services/?service_type=PHOTOGRAPHY  # حسب النوع
GET /api/extra-services/mine/               # خدمات المستخدم الحالي
POST /api/extra-services/                   # إضافة خدمة جديدة
```

### الفواتير
```http
GET /api/invoices/                          # جميع الفواتير
GET /api/invoices/mine/                     # فواتير المستخدم الحالي
POST /api/invoices/{id}/mark_paid/          # تحديد الفاتورة كمقبوضة
```

### تقارير الأرباح
```http
GET /api/revenue-reports/                   # جميع التقارير
GET /api/revenue-reports/mine/              # تقارير المستخدم الحالي
GET /api/revenue-reports/summary/           # ملخص الأرباح
```

### تفاصيل الحجز
```http
GET /api/booking-services/                 # تفاصيل الخدمات في الحجز
GET /api/booking-services/mine/            # أرباح المستخدم الحالي
```

## 💰 نظام توزيع الأرباح

### للمالك (صاحب القاعة):
- يحصل على 100% من مبلغ القاعة
- يحصل على 100% من مبلغ الكاترينج
- لا يدفع عمولة للمنصة

### لمقدمي الخدمات الإضافية:
- يحصل على 95% من مبلغ الخدمة
- تدفع المنصة 5% عمولة

### مثال على التوزيع:
```
حجز بقيمة 10,000 جنيه:
├── قاعة: 5,000 جنيه (للمالك)
├── كاترينج: 2,000 جنيه (للمالك)
├── تصوير: 2,000 جنيه (لمقدم الخدمة: 1,900 جنيه)
└── ديكور: 1,000 جنيه (لمقدم الخدمة: 950 جنيه)
```

## 🔧 إعداد النظام

### 1. تشغيل Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. إنشاء مستخدمين تجريبيين
```python
# في Django shell
from accounts.models import User

# مالك قاعة
owner = User.objects.create_user(
    username='hall_owner',
    email='owner@example.com',
    role='OWNER',
    business_type='HALL'
)

# مقدم خدمة تصوير
photographer = User.objects.create_user(
    username='photographer',
    email='photo@example.com',
    role='SERVICE',
    business_type='PHOTOGRAPHY'
)
```

### 3. إضافة خدمات إضافية
```python
# في Django shell
from services.models import ExtraService

ExtraService.objects.create(
    provider=photographer,
    name='حزمة تصوير كاملة',
    service_type='PHOTOGRAPHY',
    price=2000.00,
    description='تصوير كامل للزفاف'
)
```

## 📱 استخدام النظام

### 1. للمستخدم العادي:
1. تصفح القاعات المتاحة
2. اختر الخدمات الإضافية المطلوبة
3. أكمل بيانات الحجز
4. احصل على الفاتورة الإجمالية

### 2. لمقدمي الخدمات:
1. سجل حساب كمقدم خدمة
2. أضف خدماتك مع الأسعار
3. تابع طلبات الحجز
4. احصل على تقارير الأرباح

### 3. لأصحاب القاعات:
1. أضف قاعاتك مع الأسعار
2. تابع الحجوزات
3. احصل على الأرباح من القاعات والكاترينج

## 🎯 المميزات الرئيسية

- ✅ **حساب تلقائي للمبالغ**: النظام يحسب المبلغ الإجمالي تلقائياً
- ✅ **توزيع عادل للأرباح**: كل مقدم خدمة يحصل على نصيبه
- ✅ **فواتير مفصلة**: فاتورة إجمالية مع تفاصيل كل خدمة
- ✅ **تقارير شاملة**: تقارير الأرباح لكل مقدم خدمة
- ✅ **نظام تقسيط**: دعم خطط التقسيط المختلفة
- ✅ **إشعارات تلقائية**: إيميلات تأكيد للحجز

## 🔍 مثال عملي

```json
{
  "booking": {
    "id": 1,
    "hall": "قاعة الأفراح الكبرى",
    "date": "2024-06-15",
    "total_price": 10000.00,
    "services": [
      {
        "name": "تصوير كامل",
        "provider": "مصور محترف",
        "amount": 2000.00
      },
      {
        "name": "ديكور فاخر",
        "provider": "مصمم ديكور",
        "amount": 1500.00
      }
    ]
  },
  "invoice": {
    "invoice_number": "INV-ABC12345",
    "total_amount": 10000.00,
    "final_amount": 10000.00
  },
  "revenue_distribution": [
    {
      "provider": "مالك القاعة",
      "service": "قاعة الأفراح الكبرى",
      "amount": 6500.00
    },
    {
      "provider": "مصور محترف",
      "service": "تصوير كامل",
      "amount": 1900.00
    },
    {
      "provider": "مصمم ديكور",
      "service": "ديكور فاخر",
      "amount": 1425.00
    }
  ]
}
```

هذا النظام يوفر حلاً متكاملاً لإدارة حجوزات القاعات مع الخدمات الإضافية وتوزيع الأرباح بشكل عادل ومنظم! 🎉
