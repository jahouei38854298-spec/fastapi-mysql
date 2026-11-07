import getpass

from mysql_database import SessionLocal
from models import AdminDB
from security import hash_password


username = input("نام کاربری مدیر را وارد کنید: ").strip()

if not username:
    raise ValueError("نام کاربری نمی‌تواند خالی باشد.")

password = getpass.getpass("رمز عبور مدیر را وارد کنید: ")

if len(password) < 8:
    raise ValueError("رمز عبور باید حداقل ۸ کاراکتر باشد.")

confirm_password = getpass.getpass("رمز عبور را دوباره وارد کنید: ")

if password != confirm_password:
    raise ValueError("رمزهای عبور یکسان نیستند.")

with SessionLocal() as db:
    existing_admin = (
        db.query(AdminDB)
        .filter(AdminDB.username == username)
        .first()
    )

    if existing_admin:
        raise ValueError("این نام کاربری قبلاً ثبت شده است.")

    admin = AdminDB(
        username=username,
        hashed_password=hash_password(password),
    )

    db.add(admin)
    db.commit()

print("حساب مدیر با موفقیت ایجاد شد.")
