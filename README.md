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

### Authentication

### Halls

### Bookings

## متغيرات ال env



## الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.
