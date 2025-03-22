این هم ترجمه‌ی فایل `README.md` به فارسی:  

---

# 🚀 بهینه‌سازی پایگاه داده SQLite برای `x-ui`

این اسکریپت **پایگاه داده‌ی `x-ui` را بهینه‌سازی** می‌کند، قفل‌ها را حذف کرده و عملکرد را بهبود می‌بخشد. پس از اجرا، فایل‌های اضافی در مسیر `/etc/x-ui/` ایجاد می‌شوند که این **رفتاری طبیعی** است.

## 📌 نحوه‌ی استفاده؟

1. **اسکریپت را ذخیره کنید** در یک فایل، مثلاً `x-ui_optimize_db.py`.
2. **با دسترسی `root` اجرا کنید**:
   ```bash
   sudo python3 x_ui_optimize_db.py
   ```

## 🚀 این اسکریپت چه کارهایی انجام می‌دهد؟

### 1️⃣ متوقف کردن سرویس `x-ui`
```bash
systemctl stop x-ui
```
این کار برای جلوگیری از قفل شدن پایگاه داده در حین بهینه‌سازی ضروری است.

### 2️⃣ ایجاد یک نسخه‌ی پشتیبان در `/tmp/`
```bash
cp /etc/x-ui/x-ui.db /tmp/x-ui-<timestamp>.db
```
فایل پشتیبان شامل یک برچسب زمانی خواهد بود، مانند:
```
/tmp/x-ui-1711045600.db
```
در صورت بروز مشکل، این نسخه‌ی پشتیبان امکان بازگردانی را فراهم می‌کند.

### 3️⃣ بهینه‌سازی پایگاه داده با دستورات SQL:

| **دستور SQL** | **توضیح** |
|---------------|-------------|
| `PRAGMA journal_mode=WAL;` | حالت WAL (Write-Ahead Logging) را فعال می‌کند که **اجازه‌ی خواندن و نوشتن همزمان** را می‌دهد. این کار خطای `database locked` را کاهش می‌دهد. |
| `PRAGMA wal_checkpoint(TRUNCATE);` | فایل‌های WAL قدیمی را پاک کرده و فشار روی دیسک را کاهش می‌دهد. |
| `PRAGMA optimize;` | شاخص‌ها و کش پایگاه داده را بهینه‌سازی کرده و سرعت اجرای درخواست‌ها را افزایش می‌دهد. |
| `PRAGMA busy_timeout = 5000;` | مدت زمان انتظار قبل از نمایش خطای `database locked` را به ۵۰۰۰ میلی‌ثانیه (۵ ثانیه) افزایش می‌دهد. |
| `PRAGMA read_uncommitted = 1;` | امکان خواندن داده‌ها را بدون انتظار برای پایان تراکنش‌های دیگر فراهم می‌کند (اما ممکن است داده‌های **تأیید نشده** نمایش داده شوند). |

### 4️⃣ راه‌اندازی مجدد `x-ui` پس از بهینه‌سازی
```bash
systemctl restart x-ui
```
پس از این عملیات، پایگاه داده سریع‌تر و پایدارتر خواهد شد.

## 📂 چرا فایل‌های `x-ui.db-shm` و `x-ui.db-wal` ایجاد شده‌اند؟

پس از فعال‌سازی WAL، فایل‌های **اضافی** در مسیر `/etc/x-ui/` ظاهر می‌شوند:

| **فایل** | **توضیح** |
|----------|-------------|
| `x-ui.db` | فایل اصلی پایگاه داده SQLite. |
| `x-ui.db-wal` | فایل WAL (Write-Ahead Logging) که ابتدا تغییرات در آن ثبت می‌شوند قبل از نوشتن در فایل اصلی. |
| `x-ui.db-shm` | فایلی برای مدیریت دسترسی همزمان به داده‌ها (Shared Memory). |

**ایجاد این فایل‌ها کاملاً طبیعی است و نشانه‌ی خطا نیست.**

📌 **نکته:** اگر `x-ui.db-wal` بیش از حد بزرگ شد، می‌توانید با اجرای دستور زیر آن را پاک کنید:
```sql
PRAGMA wal_checkpoint(TRUNCATE);
```

## ✅ اگر مشکلی پیش آمد چه باید کرد؟

1. سرویس را متوقف کنید:
   ```bash
   systemctl stop x-ui
   ```  
2. پایگاه داده را از نسخه‌ی پشتیبان بازگردانی کنید:
   ```bash
   cp /tmp/x-ui-<timestamp>.db /etc/x-ui/x-ui.db
   ```  
3. سرویس را مجدداً اجرا کنید:
   ```bash
   systemctl start x-ui
   ```

## 📞 ارتباط

تلگرام: [@DSRClient](https://t.me/DSRCLIENT)
