# پروژه مدیریت کاربران با FastAPI و MySQL

این پروژه یک برنامه تحت وب برای مدیریت اطلاعات کاربران است که با استفاده از **FastAPI**، پایگاه داده **MySQL 8** و قالب‌های **Jinja2** ساخته شده است.

مدیر پس از ورود می‌تواند فهرست کاربران را مشاهده کند و عملیات افزودن، ویرایش، حذف و جست‌وجوی کاربران را انجام دهد.

این نسخه به‌صورت مستقل از نسخه MongoDB توسعه داده شده و از Docker و Docker Compose برای اجرای سرویس‌ها استفاده می‌کند.

## امکانات پروژه

- ورود مدیر و خروج از حساب کاربری
- محافظت از صفحات مدیریت با احراز هویت
- افزودن کاربر جدید
- ویرایش اطلاعات کاربران
- حذف کاربران
- نمایش فهرست کاربران
- جست‌وجوی کاربران بر اساس نام، شماره موبایل یا ایمیل
- اعتبارسنجی اطلاعات ورودی با Pydantic
- نمایش خطاهای اعتبارسنجی به زبان فارسی
- ذخیره اطلاعات در MySQL
- استفاده از SQLAlchemy برای ارتباط با پایگاه داده
- هش‌کردن رمز عبور مدیر
- محافظت از فرم‌های تغییردهنده اطلاعات با توکن CSRF
- محدودیت تلاش‌های ورود
- استفاده از SessionMiddleware برای مدیریت نشست
- طراحی صفحات با HTML و CSS
- اجرای برنامه با Uvicorn
- اجرای مستقل سرویس‌ها با Docker Compose
- نگهداری اطلاعات دیتابیس در Docker Volume

## فناوری‌های استفاده‌شده

- Python 3.10
- FastAPI
- MySQL 8.0
- SQLAlchemy
- PyMySQL
- Pydantic
- Jinja2
- HTML و CSS
- SessionMiddleware
- pwdlib
- Uvicorn
- Docker
- Docker Compose
- phpMyAdmin

## پیش‌نیازها

پیش از اجرای پروژه، موارد زیر را نصب کنید:

- Ubuntu یا یک سیستم‌عامل سازگار
- Python 3.10 یا نسخه سازگار با پروژه
- Docker
- Docker Compose Plugin
- Git (اختیاری)

برای بررسی نصب Docker:

```bash
docker --version
docker compose version
```

## ساختار فایل‌های مهم پروژه

```text
fastapi_mysql/
├── main.py
├── auth_mysql.py
├── students_mysql.py
├── mysql_database.py
├── models.py
├── schemas.py
├── security.py
├── init_db.py
├── create_admin.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
├── .env
├── README.md
├── templates/
│   ├── index.html
│   ├── add.html
│   └── login.html
├── static/
│   └── style.css
└── archive_mongodb/
```

### توضیحات فایل‌ها

- `main.py`: نقطه ورود برنامه و تنظیمات اصلی FastAPI.
- `auth_mysql.py`: مدیریت ورود مدیر، خروج و احراز هویت.
- `students_mysql.py`: مسیرهای نمایش، افزودن، ویرایش، جست‌وجو و حذف کاربران.
- `mysql_database.py`: تنظیم اتصال به MySQL و ساخت Sessionهای دیتابیس.
- `models.py`: تعریف مدل‌های پایگاه داده با SQLAlchemy.
- `schemas.py`: مدل‌ها و اعتبارسنجی اطلاعات ورودی.
- `security.py`: ابزارهای امنیتی و هش رمز عبور.
- `init_db.py`: ایجاد جدول‌های دیتابیس.
- `create_admin.py`: ایجاد حساب مدیر.
- `requirements.txt`: وابستگی‌های Python پروژه.
- `Dockerfile`: دستورالعمل ساخت تصویر Docker برنامه.
- `compose.yaml`: تنظیم سرویس‌های برنامه، MySQL و phpMyAdmin.
- `.dockerignore`: مشخص‌کردن فایل‌هایی که نباید وارد تصویر Docker شوند.
- `.gitignore`: مشخص‌کردن فایل‌هایی که نباید در Git ثبت شوند.
- `.env`: نگهداری متغیرهای محیطی و اطلاعات محرمانه.
- `templates/`: قالب‌های HTML صفحات برنامه.
- `static/style.css`: استایل صفحات وب.
- `archive_mongodb/`: نگهداری فایل‌های مرتبط با نسخه قبلی MongoDB.

## نصب و راه‌اندازی

### ۱. ورود به پوشه پروژه

```bash
cd ~/Projects/fastapi_mysql
```

### ۲. فعال‌کردن محیط مجازی

اگر محیط مجازی قبلاً ساخته شده است:

```bash
source .venv/bin/activate
```

اگر محیط مجازی وجود ندارد:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ۳. نصب وابستگی‌ها

```bash
python -m pip install -r requirements.txt
```

بررسی وابستگی‌ها:

```bash
python -m pip check
```

### ۴. تنظیم فایل محیطی

فایل `.env` باید در پوشه اصلی پروژه وجود داشته باشد.

متغیرهای موردنیاز:

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_PASSWORD=your_database_password
DATABASE_URL=mysql+pymysql://fastapi_user:your_database_password@mysql:3306/fastapi_db
SESSION_SECRET_KEY=your_secret_session_key
```

مقادیر بالا نمونه هستند و باید با رمزهای واقعی و امن جایگزین شوند.

نکات مهم:

- مقدار `MYSQL_PASSWORD` باید با رمز داخل `DATABASE_URL` یکسان باشد.
- در صورت استفاده از نویسه‌های ویژه در رمز اتصال، باید آن‌ها را به‌درستی URL Encode کنید.
- کلید `SESSION_SECRET_KEY` باید محرمانه و قوی باشد.
- فایل `.env` نباید در Git ثبت شود.
- اطلاعات محرمانه را در README یا مخزن عمومی قرار ندهید.

### ۵. اجرای سرویس‌ها با Docker Compose

برای ساخت تصویر برنامه و راه‌اندازی سرویس‌ها:

```bash
sudo docker compose up -d --build
```

بررسی وضعیت کانتینرها:

```bash
sudo docker compose ps
```

مشاهده گزارش اجرای سرویس‌ها:

```bash
sudo docker compose logs
```

مشاهده گزارش MySQL:

```bash
sudo docker compose logs mysql
```

MySQL باید وضعیت `healthy` داشته باشد.

### ۶. ایجاد جدول‌های دیتابیس

پس از فعال‌شدن سرویس MySQL، دستور زیر را اجرا کنید:

```bash
sudo docker compose exec app python init_db.py
```

در صورت موفقیت، پیام زیر نمایش داده می‌شود:

```text
Database tables created successfully.
```

این فایل جدول‌های تعریف‌شده در `models.py` را ایجاد می‌کند.

### ۷. ایجاد حساب مدیر

برای ایجاد حساب مدیر:

```bash
sudo docker compose exec app python create_admin.py
```

برنامه نام کاربری و رمز عبور را دریافت می‌کند.

رمز عبور هنگام تایپ نمایش داده نمی‌شود.

### ۸. دسترسی به برنامه

پس از راه‌اندازی موفق سرویس‌ها، آدرس‌های زیر در دسترس هستند:

- برنامه FastAPI:

  http://127.0.0.1:8001

- صفحه ورود مدیر:

  http://127.0.0.1:8001/login

- مستندات API:

  http://127.0.0.1:8001/docs

- محیط گرافیکی phpMyAdmin:

  http://127.0.0.1:8082

نکته: پورت MySQL مستقیماً روی میزبان منتشر نشده است و برنامه از طریق شبکه داخلی Docker به سرویس MySQL متصل می‌شود.

## نحوه استفاده

۱. صفحه ورود مدیر را باز کنید.

۲. با اطلاعات حساب مدیر وارد شوید.

۳. فهرست کاربران را مشاهده کنید.

۴. برای افزودن کاربر، فرم افزودن کاربر جدید را باز کنید.

۵. برای ویرایش، گزینه مربوط به کاربر موردنظر را انتخاب کنید.

۶. برای حذف، از گزینه حذف کاربر استفاده کنید.

۷. برای جست‌وجوی کاربران از کادر جست‌وجو استفاده کنید.

۸. پس از پایان کار از حساب مدیر خارج شوید.

## اطلاعات کاربران

مدل اطلاعات کاربران شامل فیلدهای زیر است:

- شناسه
- نام
- سن
- تاریخ تولد
- نام پدر
- محل تولد
- شماره موبایل
- ایمیل
- آدرس

تعریف دقیق فیلدها و محدودیت‌های آن‌ها در فایل‌های `models.py` و `schemas.py` قرار دارد.

## پایگاه داده MySQL

نام دیتابیس:

```text
fastapi_db
```

نام کاربر دیتابیس برنامه:

```text
fastapi_user
```

جدول‌های اصلی:

```text
students
admins
```

جدول `students` اطلاعات کاربران را نگهداری می‌کند.

جدول `admins` اطلاعات حساب‌های مدیر و رمزهای هش‌شده را نگهداری می‌کند.

## مدیریت Docker

### مشاهده وضعیت سرویس‌ها

```bash
sudo docker compose ps
```

### راه‌اندازی سرویس‌ها

```bash
sudo docker compose up -d
```

### متوقف‌کردن سرویس‌ها

```bash
sudo docker compose stop
```

### راه‌اندازی مجدد سرویس‌ها

```bash
sudo docker compose restart
```

### راه‌اندازی مجدد فقط برنامه FastAPI

```bash
sudo docker compose restart app
```

### مشاهده گزارش برنامه

```bash
sudo docker compose logs -f app
```

### ورود به محیط MySQL

```bash
sudo docker compose exec mysql mysql -u fastapi_user -p fastapi_db
```

رمز عبور کاربر دیتابیس را در زمان درخواست وارد کنید.

## پشتیبان‌گیری از دیتابیس

اطلاعات MySQL در Volume زیر نگهداری می‌شوند:

```text
fastapi_mysql_project_mysql_data
```

برای تهیه نسخه پشتیبان از دیتادایرکتوری MySQL، ابتدا سرویس دیتابیس را متوقف کنید:

```bash
sudo docker compose stop mysql
```

سپس در پوشه پروژه اجرا کنید:

```bash
sudo docker run --rm \
  -v fastapi_mysql_project_mysql_data:/source:ro \
  -v "$PWD":/backup \
  docker.arvancloud.ir/mysql:8.0 \
  tar -czf /backup/mysql_data_backup.tar.gz -C /source .
```

پس از پایان پشتیبان‌گیری، سرویس MySQL را دوباره اجرا کنید:

```bash
sudo docker compose up -d mysql
```

بررسی فایل پشتیبان:

```bash
ls -lh mysql_data_backup.tar.gz
```

این روش از دیتادایرکتوری در حالت توقف MySQL نسخه پشتیبان می‌گیرد.

فایل‌های پشتیبان را در محل امن نگهداری کنید و آن‌ها را در مخزن Git قرار ندهید.

## حفظ اطلاعات

اطلاعات دیتابیس در Docker Volume ذخیره می‌شوند؛ بنابراین با Restart یا راه‌اندازی مجدد کانتینرها حذف نمی‌شوند.

برای راه‌اندازی مجدد سرویس‌ها:

```bash
sudo docker compose restart
```

برای مشاهده Volume:

```bash
sudo docker volume ls
```

**هشدار:** از اجرای دستور زیر بدون داشتن نسخه پشتیبان و آگاهی کامل از پیامدهای آن خودداری کنید:

```bash
sudo docker compose down -v
```

گزینه `-v` می‌تواند Volumeهای پروژه را حذف کند و باعث از بین رفتن اطلاعات دیتابیس شود.

## نکات امنیتی

- رمز عبور مدیر باید به‌صورت هش‌شده نگهداری شود.
- کلید محرمانه نشست باید از طریق متغیر محیطی تنظیم شود.
- فایل `.env` را در Git ثبت نکنید.
- از رمزهای عبور قوی استفاده کنید.
- محافظت CSRF را برای فرم‌های تغییردهنده اطلاعات غیرفعال نکنید.
- در محیط عملیاتی از HTTPS استفاده کنید.
- در محیط عملیاتی تنظیم `https_only` برای کوکی نشست باید فعال باشد.
- در محیط عملیاتی حالت توسعه و `--reload` را فعال نگذارید.
- تلاش‌های ورود ناموفق را محدود کنید.
- از دیتابیس به‌صورت منظم نسخه پشتیبان تهیه کنید.
- فایل‌های پشتیبان را در محل امن و جداگانه نگهداری کنید.
- برای دسترسی عمومی به برنامه، تنظیمات شبکه و دسترسی‌های Docker را بررسی کنید.

## مدیریت وابستگی‌ها

برای بررسی سلامت وابستگی‌ها:

```bash
python -m pip check
```

برای بررسی قابل‌کامپایل بودن فایل‌های Python:

```bash
python -m compileall -q .
```

در صورت تغییر کتابخانه‌ها، فایل `requirements.txt` را به‌روزرسانی کنید.

## تفاوت با نسخه MongoDB

این پروژه نسخه مستقل MySQL از برنامه مدیریت کاربران است.

- نسخه قبلی از MongoDB و PyMongo استفاده می‌کند.
- نسخه جدید از MySQL و SQLAlchemy استفاده می‌کند.
- هر پروژه تنظیمات، کانتینرها و پایگاه داده مستقل دارد.
- دیتابیس نسخه MongoDB به‌صورت خودکار به نسخه MySQL منتقل نمی‌شود.
- اجرای پروژه MySQL نباید باعث حذف یا تغییر اطلاعات نسخه MongoDB شود.

## مجوز

در صورت انتشار عمومی پروژه، مجوز مناسب را مطابق شرایط استفاده و نیازهای خود به مخزن اضافه کنید.
