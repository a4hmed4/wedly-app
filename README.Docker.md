# WedlyApp - Docker Deployment Guide

## 🐳 **Docker Deployment (بدون Cloud Build)**

### **الملفات المطلوبة:**
- ✅ `Dockerfile` - إعدادات Docker محسّنة
- ✅ `docker-deploy.sh` - سكريبت الرفع التلقائي
- ❌ `cloudbuild.yaml` - تم حذفه

## 🚀 **طريقة الرفع:**

### **1. الرفع التلقائي (مُوصى به):**
```bash
# تشغيل السكريبت
./docker-deploy.sh
```

### **2. الرفع اليدوي:**
```bash
# 1. بناء الصورة
docker build -t gcr.io/wedly-app-475621/wedlyapp .

# 2. رفع الصورة
docker push gcr.io/wedly-app-475621/wedlyapp

# 3. نشر على Cloud Run
gcloud run deploy wedlyapp \
    --image gcr.io/wedly-app-475621/wedlyapp \
    --platform managed \
    --region me-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --timeout 300 \
    --concurrency 100 \
    --set-env-vars "DEBUG=False,SECRET_KEY=your-secret-key-here,ALLOWED_HOSTS=wedly-app-258355634687.me-central1.run.app,PORT=8080,DJANGO_SETTINGS_MODULE=wedding_project.settings,DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres"
```

## 🔧 **إعدادات Dockerfile:**

### **المميزات:**
- ✅ **Dynamic Port**: يستخدم متغير البيئة `PORT`
- ✅ **Health Check**: فحص صحة التطبيق
- ✅ **Startup Script**: إعداد Django تلقائي
- ✅ **Database Support**: دعم SQLite و PostgreSQL
- ✅ **Static Files**: جمع الملفات الثابتة
- ✅ **Migrations**: تشغيل migrations تلقائياً

### **Environment Variables:**
```bash
# Required
PORT=8080
DJANGO_SETTINGS_MODULE=wedding_project.settings

# Optional (for Supabase)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres

# Optional (for production)
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=wedly-app-258355634687.me-central1.run.app
```

## 📋 **خطوات الرفع:**

### **1. إعداد Google Cloud:**
```bash
# تسجيل الدخول
gcloud auth login

# تعيين المشروع
gcloud config set project wedly-app-475621

# تفعيل APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### **2. إعداد Docker:**
```bash
# تكوين Docker للـ GCR
gcloud auth configure-docker

# أو استخدام Docker Desktop مع Google Cloud
```

### **3. تحديث كلمة المرور:**
```bash
# في docker-deploy.sh أو الأمر اليدوي
# استبدل [YOUR_PASSWORD] بكلمة المرور الفعلية من Supabase
DATABASE_URL=postgresql://postgres:your-actual-password@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres
```

### **4. الرفع:**
```bash
# تشغيل السكريبت
./docker-deploy.sh
```

## 🔍 **استكشاف الأخطاء:**

### **مشاكل شائعة:**
1. **Docker Build Failed**: تحقق من `requirements.txt`
2. **Push Failed**: تحقق من `gcloud auth configure-docker`
3. **Deploy Failed**: تحقق من `DATABASE_URL` و `SECRET_KEY`

### **أوامر مفيدة:**
```bash
# فحص الصورة
docker images | grep wedlyapp

# تشغيل محلي
docker run -p 8080:8080 gcr.io/wedly-app-475621/wedlyapp

# فحص logs
gcloud run services logs wedlyapp --region me-central1
```

## 📊 **المراقبة:**

### **Cloud Run Console:**
- **URL**: `https://wedly-app-258355634687.me-central1.run.app`
- **Logs**: Cloud Run → wedlyapp → Logs
- **Metrics**: Cloud Run → wedlyapp → Metrics

### **Supabase Dashboard:**
- **Database**: مراقبة قاعدة البيانات
- **Logs**: سجلات الاتصال
- **Performance**: إحصائيات الأداء

## 🎯 **المميزات:**

- ✅ **Simplified**: Docker فقط بدون Cloud Build
- ✅ **Flexible**: دعم SQLite و PostgreSQL
- ✅ **Automated**: سكريبت رفع تلقائي
- ✅ **Production Ready**: جاهز للإنتاج
- ✅ **Monitoring**: مراقبة شاملة

## 📞 **الدعم:**

- **Docker Docs**: [docs.docker.com](https://docs.docker.com)
- **Cloud Run Docs**: [cloud.google.com/run](https://cloud.google.com/run)
- **Supabase Docs**: [docs.supabase.com](https://docs.supabase.com)