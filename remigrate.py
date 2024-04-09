import os
import subprocess
from sys import argv

if len(argv) < 4:
    raise Exception("Введите в строку параметров superuser_name superuser_password port через пробел")
script, admin_name, admin_password, port = argv

if os.path.exists("db.sqlite3"):
    os.remove("db.sqlite3")
open("db.sqlite3", "w").close()

for app in os.listdir("."):
    if os.path.isdir(app) and os.path.exists(os.path.join(app, "migrations")):
        migrations_dir = os.path.join(app, "migrations")
        for file in os.listdir(migrations_dir):
            if file.endswith(".py") and file != "__init__.py":
                os.remove(os.path.join(migrations_dir, file))

subprocess.run(["py", "manage.py", "makemigrations"])
subprocess.run(["py", "manage.py", "migrate"])
os.environ['DJANGO_SUPERUSER_PASSWORD'] = admin_password
os.system(f'py manage.py createsuperuser --username={admin_name} --email=admin@example.com --noinput')

print("Ремиграция успешно выполена")
print(f"Суперпользователь создан с логином: {admin_name} и паролем: {admin_password}")
print(f"Сервер запущен на порте: {port}")
subprocess.run(["py", "manage.py", "runserver", port])
