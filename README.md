# Wedly App

تطبيق لإدارة حجز قاعات الأفراح باستخدام Django REST Framework.

## التقنيات المستخدمة

- **Backend**: Django 5.2.7
- **API**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (Development)
- **Image Processing**: Pillow

## التثبيت والتشغيل

### 1. تنزيل البروجيكت
```bash
git clone <repository-url>
cd wedding-app
```

### 2. إنشاء ال environment
```bash
python -m venv venv
```

### 3. تفعيل ال environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. تثبيت ال Requirements
```bash
pip install -r requirements.txt
```

### 5. إعداد ال Environment
```bash
# انسخ ملف .env.example إلى .env
cp .env.example .env

# قم بتعديل القيم في ملف .env
```

### 6. تشغيل المايجريشن
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. createsuperuser للأدمن بانل
```bash
python manage.py createsuperuser
```

### 8. تشغيل ال Server
```bash
python manage.py runserver
```

## هيكل المشروع

```
wedding-app/
├── accounts/          # إدارة المستخدمين
├── halls/            # إدارة القاعات
├── notifications/    # نظام الإشعارات
├── bookings/         # نظام الحجز
├── services/    # نظام الخدمات
├── payments/    # نظام الدفع
├── wedding_project/  # إعدادات المشروع الرئيسية
├── requirements.txt  # متطلبات المشروع
└── manage.py        # ملف إدارة Django
```

## API Endpoints

### Authentication & Accounts
- POST `/api/accounts/register/`
- POST `/api/token/`
- POST `/api/token/refresh/`
- GET `/api/accounts/profile/`
- GET `/api/accounts/dashboard/user/`
- GET `/api/accounts/dashboard/owner/`
- GET `/api/accounts/dashboard/service/`
- GET `/api/accounts/dashboard/admin/`

### Halls
- GET `/api/halls/venues/`
- POST `/api/halls/create/` (Owner)
- PATCH `/api/halls/venues/{id}/update/` (Owner)
- DELETE `/api/halls/venues/{id}/delete/` (Owner)
- GET `/api/halls/halls/`
- POST `/api/halls/halls/` (Owner)
- PATCH `/api/halls/halls/{id}/` (Owner)
- DELETE `/api/halls/halls/{id}/` (Owner)

### Services
- GET `/api/services/services/`
- POST `/api/services/services/` (Service Provider)
- PATCH `/api/services/services/{id}/` (Service Provider)
- DELETE `/api/services/services/{id}/` (Service Provider)
- GET `/api/services/services/mine/` (Service Provider)

### Bookings
- GET `/api/bookings/book/` (My bookings)
- POST `/api/bookings/book/`
- PATCH `/api/bookings/book/{id}/`
- DELETE `/api/bookings/book/{id}/`

### Reviews
- GET `/api/reviews/reviews/`
- POST `/api/reviews/reviews/`
- PATCH `/api/reviews/reviews/{id}/`
- DELETE `/api/reviews/reviews/{id}/`

### Payments
- GET `/api/payments/payments/`

### Cloud (Firestore)
- GET `/api/cloud/fs/{collection}/?page_size=10&cursor=<docId>&order_by=<field>&where=field,==,value`

## متغيرات ال env

لتمكين Firestore:
```
FIRESTORE_ENABLED=true
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_JSON=path/to/service-account.json
API_PAGE_SIZE=10
```

## Postman
- Import collection: `postman/WeddingApp.postman_collection.json`
- Import environment: `postman/WeddingApp.postman_environment.json`
- خطوات التجربة:
  1) سجل مستخدمين للأدوار المختلفة أو حدّث الدور من الأدمن بانل
  2) احصل على `access` من `/api/token/` وضعه في متغير البيئة المناسب
  3) جرّب CRUD عبر الطلبات الجاهزة
  4) للـ pagination استخدم `?page_size=` وروابط `next` في DRF أو `next_cursor` في Firestore



## الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.
