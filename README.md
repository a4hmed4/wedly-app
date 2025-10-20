# 🎉 WedlyApp - منصة حجز قاعات الأفراح والخدمات المتكاملة

> **الإصدار الحالي:** v1.1.0 | **آخر تحديث:** 2025

## 📖 نظرة عامة

WedlyApp هو تطبيق ويب متكامل لإدارة حجز قاعات الأفراح والخدمات المرتبطة بها، مبني باستخدام Django REST Framework مع دعم قاعدة بيانات Supabase و Firebase. يتميز بواجهة APIs مبسطة بدون `/api/` prefix لسهولة الاستخدام.

## ✨ المميزات الرئيسية

### 👥 إدارة المستخدمين
- تسجيل المستخدمين مع أدوار مختلفة (Admin, Owner, Service Provider, User)
- نظام مصادقة متقدم مع JWT
- ملفات شخصية مخصصة لكل نوع مستخدم
- لوحات تحكم مختلفة لكل دور

### 🏢 إدارة القاعات
- إضافة وإدارة قاعات الأفراح
- عرض القاعات المميزة
- نظام حجز متقدم
- إدارة المواعيد المتاحة

### 🔧 إدارة الخدمات
- إضافة وإدارة الخدمات المختلفة
- واجهات مخصصة لمقدمي الخدمات
- نظام تقييم الخدمات
- إدارة الأسعار والعروض

### 📅 نظام الحجوزات
- حجز متكامل للقاعات والخدمات
- تتبع حالة الحجوزات
- إشعارات تلقائية
- إدارة المواعيد

### 💳 نظام المدفوعات
- معالجة المدفوعات الآمنة
- إيصالات PDF
- تتبع المدفوعات
- نظام الأقساط

### ⭐ نظام التقييمات
- تقييم القاعات والخدمات
- عرض التقييمات والمراجعات
- نظام النجوم المتقدم

### 🔔 نظام الإشعارات
- إشعارات فورية
- إشعارات البريد الإلكتروني
- تتبع حالة الإشعارات

## 🚀 التقنيات المستخدمة

### Backend
- **Django 5.2.7** - إطار عمل Python
- **Django REST Framework** - لبناء APIs
- **JWT Authentication** - للمصادقة الآمنة
- **PostgreSQL** - قاعدة البيانات الرئيسية (Supabase)
- **SQLite** - للتطوير المحلي


### Cloud Services
- **Google Cloud Run** - استضافة التطبيق
- **Supabase** - قاعدة البيانات السحابية
- **Google Container Registry** - تخزين الصور

## 📋 متطلبات النظام

- Python 3.11+
- Django 5.2.7
- PostgreSQL (Supabase)
- Docker (اختياري)

## 🛠️ التثبيت والتشغيل

### 1. استنساخ المشروع
```bash
git clone https://github.com/your-username/wedlyapp.git
cd wedlyapp
```

### 2. إعداد البيئة الافتراضية
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة
```bash
cp env.example .env
# عدّل ملف .env مع بياناتك
```

### 5. تشغيل Migrations
```bash
python manage.py migrate
```

### 6. إنشاء Superuser
```bash
python manage.py createsuperuser
```

### 7. تشغيل الخادم
```bash
python manage.py runserver
```

## 🌐 APIs المتاحة

> **ملاحظة:** جميع  متاحة مباشرة لسهولة الاستخدام

### 👥 إدارة المستخدمين
- `POST /accounts/register/` - تسجيل مستخدم جديد
- `POST /accounts/login/` - تسجيل الدخول  
- `GET /accounts/profile/` - الملف الشخصي
- `GET /accounts/dashboard/user/` - لوحة المستخدم
- `GET /accounts/dashboard/admin/` - لوحة الإدارة
- `GET /accounts/dashboard/owner/` - لوحة المالك
- `GET /accounts/dashboard/service/` - لوحة مقدم الخدمة

### 🏢 إدارة القاعات
- `GET /halls/` - قائمة القاعات
- `POST /halls/` - إضافة قاعة جديدة
- `GET /halls/featured/` - القاعات المميزة

### 🔧 إدارة الخدمات
- `GET /services/` - قائمة الخدمات
- `POST /services/` - إضافة خدمة جديدة
- `GET /services/storefront/` - واجهة المتجر
- `GET /services/schema/` - مخطط الخدمات

### 📅 إدارة الحجوزات
- `GET /bookings/` - قائمة الحجوزات
- `POST /bookings/` - حجز جديد
- `GET /bookings/my-bookings/` - حجوزاتي

### 💳 إدارة المدفوعات
- `GET /payments/` - قائمة المدفوعات
- `POST /payments/` - دفعة جديدة
- `GET /payments/receipt/{id}/` - إيصال الدفع

### ⭐ إدارة التقييمات
- `GET /reviews/` - قائمة التقييمات
- `POST /reviews/` - تقييم جديد

### 🔔 إدارة الإشعارات
- `GET /notifications/` - قائمة الإشعارات
- `POST /notifications/` - إشعار جديد
- `PUT /notifications/mark-read/{id}/` - تحديد كمقروء

### ☁️ قاعدة البيانات السحابية
- `GET /cloud/collections/` - المجموعات
- `GET /cloud/collections/users/` - مستخدمي Firebase

### 🔐 المصادقة
- `POST /token/` - الحصول على JWT Token
- `POST /token/refresh/` - تجديد JWT Token
- `POST /auth/login/` - تسجيل الدخول (dj-rest-auth)
- `POST /auth/logout/` - تسجيل الخروج
- `POST /auth/registration/` - تسجيل جديد

## 🎨 واجهة المستخدم الجديدة

### ✨ مميزات الواجهة
- **تصميم جميل ومتجاوب** - يعمل على جميع الأجهزة
- **دعم اللغة العربية** - واجهة باللغة العربية كاملة
- **روابط مباشرة** - وصول سهل لجميع APIs
- **تصنيف منظم** - APIs مقسمة حسب الوظيفة

### 🚀 كيفية الاستخدام
1. **زيارة الصفحة الرئيسية**: `https://wedly-app-258355634687.me-central1.run.app/`
2. **اختيار API** من القوائم المنظمة
3. **النقر على الرابط** للانتقال مباشرة للـ API
4. **استخدام Admin Panel** من الرابط المخصص

## 🐳 النشر باستخدام Docker

### 1. بناء الصورة
```bash
docker build -t gcr.io/wedly-app-475621/wedlyapp .
```

### 2. رفع الصورة
```bash
docker push gcr.io/wedly-app-475621/wedlyapp
```

### 3. النشر على Cloud Run
```bash
./deploy.sh
```

## 🌍 النشر على Google Cloud Run

### 1. إعداد Google Cloud
```bash
gcloud auth login
gcloud config set project wedly-app-475621
```

### 2. النشر التلقائي
```bash
./deploy.sh
```

### 3. تشغيل Migrations
```bash
./run-migrations.sh
```

## 📱 واجهات المستخدم

### 🏠 الصفحة الرئيسية
- **URL**: `https://wedly-app-258355634687.me-central1.run.app/`
- عرض جميع APIs المتاحة مع تصميم جميل
- روابط مباشرة لجميع الخدمات
- واجهة عربية متجاوبة

### ⚙️ لوحة التحكم الإدارية
- **URL**: `https://wedly-app-258355634687.me-central1.run.app/admin/`
- إدارة كاملة للنظام
- بيانات الدخول الافتراضية: `admin/admin123`
- صفحة وصول سهلة: `https://wedly-app-258355634687.me-central1.run.app/admin-access/`

### 📋 معلومات APIs
- **URL**: `https://wedly-app-258355634687.me-central1.run.app/api-info/`
- معلومات مفصلة عن جميع APIs في JSON format
- URLs محدثة بدون `/api/` prefix

## 🔐 الأمان

- JWT Authentication
- CORS Configuration
- HTTPS Enforcement
- Environment Variables Protection
- SQL Injection Prevention
- XSS Protection

## 📊 قاعدة البيانات

### Supabase (الإنتاج)
- PostgreSQL Database
- Real-time Subscriptions
- Row Level Security
- Automatic Backups

### SQLite (التطوير)
- قاعدة بيانات محلية
- سهولة التطوير والاختبار

## 🧪 الاختبار

```bash
# تشغيل الاختبارات
python manage.py test

# اختبار APIs باستخدام Postman
# استخدم ملف: postman/WeddingApp.postman_collection.json
```

### 🌐 اختبار URLs الجديدة

```bash
# اختبار الصفحة الرئيسية
curl https://wedly-app-258355634687.me-central1.run.app/

# اختبار APIs بدون /api/ prefix
curl https://wedly-app-258355634687.me-central1.run.app/accounts/
curl https://wedly-app-258355634687.me-central1.run.app/halls/
curl https://wedly-app-258355634687.me-central1.run.app/services/

# اختبار معلومات APIs
curl https://wedly-app-258355634687.me-central1.run.app/api-info/
```

## 📈 المراقبة والأداء

- Django Debug Toolbar
- Logging Configuration
- Performance Monitoring
- Error Tracking
- Health Checks


## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 📞 الدعم

- **البريد الإلكتروني**: support@wedlyapp.com
- **الموقع الرسمي**: https://wedlyapp.com
- **GitHub Issues**: [فتح issue جديد](https://github.com/your-username/wedlyapp/issues)

## 🎯 Roadmap

- [x] ✅ APIs بدون `/api/` prefix لسهولة الاستخدام
- [x] ✅ صفحة APIs Dashboard جميلة ومتجاوبة
- [x] ✅ لوحة تحكم إدارية سهلة الوصول
- [x] ✅ دعم قاعدة بيانات Supabase
- [x] ✅ نشر على Google Cloud Run
- [ ] 🔄 تطبيق الهاتف المحمول
- [ ] 🔄 نظام الدفع الإلكتروني المتقدم
- [ ] 🔄 ذكاء اصطناعي لتوصية الخدمات
- [ ] 🔄 نظام الشحن والتوصيل
- [ ] 🔄 تطبيق Desktop

## 🆕 آخر التحديثات

### v1.1.0 (2025)
- ✅ إزالة `/api/` prefix من جميع URLs
- ✅ إنشاء صفحة APIs Dashboard جميلة
- ✅ إضافة صفحة وصول للوحة التحكم الإدارية
- ✅ تحديث جميع الوثائق والتوثيق
- ✅ تحسين تجربة المستخدم

### v1.0.0 (2025)
- ✅ إطلاق المشروع الأساسي
- ✅ APIs متكاملة لجميع الوحدات
- ✅ دعم قاعدة بيانات Supabase
- ✅ نشر على Google Cloud Run

---

**تم تطويره بـ ❤️ باستخدام Django REST Framework**