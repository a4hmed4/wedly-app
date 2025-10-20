# WedlyApp - Supabase Database Setup

## 🗄️ **إعداد قاعدة البيانات مع Supabase**

### **1. إنشاء مشروع Supabase:**
1. اذهب إلى [supabase.com](https://supabase.com)
2. أنشئ حساب جديد أو سجل الدخول
3. أنشئ مشروع جديد
4. اختر اسم المشروع والمنطقة

### **2. الحصول على معلومات الاتصال:**
1. اذهب إلى **Settings** → **Database**
2. انسخ **Connection string** من قسم **Connection pooling**
3. استبدل `[YOUR_PASSWORD]` بكلمة المرور الفعلية

### **3. تحديث كلمة المرور:**

#### **في Dockerfile:**
```dockerfile
ENV DATABASE_URL=postgresql://postgres:your-actual-password@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres
```

#### **في deploy.sh:**
```bash
DATABASE_URL=postgresql://postgres:your-actual-password@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres
```

### **4. الرفع على Cloud Run:**
```bash
# تحديث كلمة المرور في الملفات
# ثم تشغيل السكريبت
./deploy.sh
```

## 🔧 **إعدادات قاعدة البيانات**

### **Django Settings:**
```python
# wedding_project/settings.py
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
    )
}
```

### **متطلبات إضافية:**
```
psycopg2-binary==2.9.9
dj-database-url==2.3.0
```

## 🚀 **النشر على Cloud Run**

### **1. تحديث كلمة المرور:**
```bash
# في Dockerfile
ENV DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres

# في deploy.sh
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres
```

### **2. رفع التطبيق:**
```bash
./deploy.sh
```

## 📊 **مميزات Supabase:**

- ✅ **PostgreSQL**: قاعدة بيانات قوية وموثوقة
- ✅ **Real-time**: تحديثات فورية
- ✅ **Authentication**: نظام مصادقة مدمج
- ✅ **Storage**: تخزين الملفات
- ✅ **Dashboard**: لوحة تحكم سهلة
- ✅ **API**: REST API تلقائي

## 🔒 **الأمان:**

1. **كلمة المرور**: استخدم كلمة مرور قوية
2. **SSL**: الاتصال مشفر تلقائياً
3. **Row Level Security**: أمان على مستوى الصفوف
4. **Backup**: نسخ احتياطية تلقائية

## 📈 **المراقبة:**

1. **Supabase Dashboard**: مراقبة الأداء
2. **Logs**: سجلات مفصلة
3. **Metrics**: إحصائيات الاستخدام
4. **Alerts**: تنبيهات الأخطاء

## 🛠️ **استكشاف الأخطاء:**

### **مشاكل شائعة:**
1. **Connection Failed**: تحقق من كلمة المرور
2. **SSL Error**: تأكد من الاتصال المشفر
3. **Timeout**: تحقق من إعدادات الشبكة

### **أوامر مفيدة:**
```bash
# اختبار الاتصال
python manage.py dbshell

# فحص migrations
python manage.py showmigrations

# إنشاء superuser
python manage.py createsuperuser
```

## 📞 **الدعم:**

- **Supabase Docs**: [docs.supabase.com](https://docs.supabase.com)
- **Django Docs**: [docs.djangoproject.com](https://docs.djangoproject.com)
- **Community**: [github.com/supabase/supabase](https://github.com/supabase/supabase)
