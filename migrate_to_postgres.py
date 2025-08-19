import os
import json
import subprocess

# ---------- 1. تنظیمات پروژه ----------
# مسیر manage.py
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# تنظیمات دیتابیس PostgreSQL
DB_NAME = "smartshoppingdb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5432"

# ---------- 2. مسیر settings.py ----------
SETTINGS_FILE = os.path.join(PROJECT_DIR, "smartshopping", "settings.py")  # مسیر پروژه رو درست کن

# ---------- 3. گرفتن خروجی از SQLite ----------
print("📦 در حال خروجی گرفتن دیتا از SQLite...")
subprocess.run(
    ["python", "manage.py", "dumpdata", "--exclude", "auth.permission", "--exclude", "contenttypes", "--indent", "2", "-o", "data.json"],
    cwd=PROJECT_DIR
)

# ---------- 4. تغییر settings.py ----------
print("✏️ تغییر فایل settings.py به PostgreSQL...")
with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
    settings_content = f.read()

new_db_config = f"""
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{DB_NAME}',
        'USER': '{DB_USER}',
        'PASSWORD': '{DB_PASSWORD}',
        'HOST': '{DB_HOST}',
        'PORT': '{DB_PORT}',
    }}
}}
"""

import re
settings_content = re.sub(r"DATABASES\s*=\s*\{.*?\}\s*", new_db_config, settings_content, flags=re.S)

with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
    f.write(settings_content)

# ---------- 5. ایجاد دیتابیس PostgreSQL ----------
print("🛠 ایجاد دیتابیس PostgreSQL...")
create_db_cmd = f"""
psql -U postgres -c "CREATE DATABASE {DB_NAME};"
psql -U postgres -c "CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};"
"""
subprocess.run(create_db_cmd, shell=True)

# ---------- 6. مهاجرت به PostgreSQL ----------
print("🔄 اجرای migrate روی PostgreSQL...")
subprocess.run(["python", "manage.py", "migrate"], cwd=PROJECT_DIR)

# ---------- 7. وارد کردن دیتا ----------
print("📥 وارد کردن دیتا به PostgreSQL...")
subprocess.run(["python", "manage.py", "loaddata", "data.json"], cwd=PROJECT_DIR)

print("✅ successfully")
