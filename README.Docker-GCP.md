# WedlyApp - Docker على Google Cloud

## 🐳 خيارات Docker على Google Cloud:

### 1. **Google Cloud Run** (الأسهل والأرخص)
- Serverless مع Docker
- دفع فقط عند الاستخدام
- Auto-scaling تلقائي

### 2. **Google Kubernetes Engine (GKE)**
- Kubernetes cluster كامل
- تحكم كامل
- مناسب للمشاريع الكبيرة

### 3. **Compute Engine**
- VPS عادي مع Docker
- أرخص للاستخدام المستمر
- تحكم كامل

## 🚀 الرفع السريع - Cloud Run:

### 1. إعداد Google Cloud:
```bash
# تثبيت Google Cloud SDK
# تسجيل الدخول
gcloud auth login

# تحديد المشروع
gcloud config set project YOUR_PROJECT_ID
```

### 2. تشغيل الرفع:
```bash
# جعل السكريبت قابل للتنفيذ
chmod +x gcp-docker-deploy.sh

# تشغيل الرفع
./gcp-docker-deploy.sh
```

### 3. إعداد متغيرات البيئة:
في Google Cloud Console:
- اذهب إلى Cloud Run
- اختر خدمتك
- اذهب إلى "Edit & Deploy New Revision"
- أضف Environment Variables:
  ```
  SECRET_KEY=your-secret-key
  DEBUG=False
  ALLOWED_HOSTS=your-service-url
  DATABASE_URL=sqlite:///db.sqlite3
  ```

## 🔧 إعدادات Dockerfile للـ Cloud Run:

Dockerfile الحالي جاهز للـ Cloud Run:
- ✅ Port 8080
- ✅ Non-root user
- ✅ Health checks
- ✅ Static files

## 💰 التكلفة:

| الخدمة | التكلفة |
|--------|---------|
| **Cloud Run** | $0.40/مليون طلب + $0.00002400/GB-second |
| **GKE** | $0.10/ساعة للـ cluster |
| **Compute Engine** | $5-20/شهر حسب المواصفات |

## 🎯 التوصيات:

### للتطوير/الاختبار:
- **Cloud Run**: سهل وسريع

### للإنتاج:
- **Cloud Run**: إذا كان الاستخدام متقطع
- **Compute Engine**: إذا كان الاستخدام مستمر
- **GKE**: إذا كنت تحتاج Kubernetes

## 🔄 مقارنة سريعة:

| الميزة | Cloud Run | GKE | Compute Engine |
|--------|------------|-----|----------------|
| **السهولة** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **التكلفة** | حسب الاستخدام | ثابت | ثابت |
| **التحكم** | محدود | كامل | كامل |
| **Auto-scaling** | تلقائي | تلقائي | يدوي |

## 🚀 أي خيار تفضل؟

1. **Cloud Run** (الأسهل)
2. **Compute Engine** (أرخص للاستخدام المستمر)
3. **GKE** (للمشاريع الكبيرة)
