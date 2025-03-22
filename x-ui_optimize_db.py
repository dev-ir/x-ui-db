import os
import sqlite3
import time

db_path = "/etc/x-ui/x-ui.db"
backup_path = f"/tmp/x-ui-{int(time.time())}.db"

os.system("systemctl stop x-ui")
print("Сервис x-ui остановлен.")

os.system(f"cp {db_path} {backup_path}")
print(f"Бэкап создан: {backup_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    commands = [
        "PRAGMA journal_mode=WAL;",
        "PRAGMA wal_checkpoint(TRUNCATE);",
        "PRAGMA optimize;",
        "PRAGMA busy_timeout = 5000;",
        "PRAGMA read_uncommitted = 1;"
    ]

    for cmd in commands:
        cursor.execute(cmd)
        result = cursor.fetchone()
        print(f"🔹 {cmd} -> {result}")

    conn.commit()
    conn.close()
    print("Оптимизация базы данных завершена.")

    os.system("systemctl restart x-ui")
    print("Сервис x-ui запущен.")
    print("База данных успешно оптимизирована!")
    print("Добро пожаловать в сообщество @XrayUI")

except Exception as e:
    print(f"❌ Ошибка: {e}")
