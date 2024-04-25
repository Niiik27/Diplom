import os
import subprocess
from sys import argv
import subprocess
def update_requirements_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        updated_lines = [line.replace('==', '>=') for line in lines]
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)
        print("requirements успешно обновлен до последней версии.")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")

# Пример использования функции

# Запуск команды "pip freeze --upgrade" и запись вывода в файл
with open("requirements.txt", "w") as f:
    result = subprocess.run(["pip", "freeze"], stdout=f, text=True)

# Проверка статуса выполнения команды
if result.returncode == 0:
    print("Зависимости обновлены")
else:
    print("Не удалось обновить зависимости:", result.stderr)
update_requirements_file('requirements.txt')

def get_project_name():
    current_dir = os.path.abspath(os.getcwd())
    for dirpath, dirnames, filenames in os.walk(current_dir):
        if 'venv' in dirnames:
            dirnames.remove('venv')
        if 'settings.py' in filenames:
            return os.path.basename(dirpath)
    raise FileNotFoundError("Файл settings.py не найден в текущем каталоге или его родительских каталогах.")

project_name = get_project_name()
print(f"Имя проекта: {project_name}")
def remigrate():
    if len(argv) < 4:
        raise Exception("Введите в строку параметров superuser_name superuser_password port через пробел")
    script, admin_name, admin_password, port = argv
    # subprocess.run(["py", "manage.py", "flush"])
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
    open("db.sqlite3", "w").close()

    for app in os.listdir("."):
        if os.path.isdir(app) and os.path.exists(os.path.join(app, "migrations")):
            migrations_dir = os.path.join(app, "migrations")
            for file in os.listdir(migrations_dir):
                print(file)
                if file.endswith(".py") and file != "__init__.py":
                    os.remove(os.path.join(migrations_dir, file))

    subprocess.run(["py", "manage.py", "makemigrations"])
    subprocess.run(["py", "manage.py", "migrate"])
    os.environ['DJANGO_SUPERUSER_PASSWORD'] = admin_password
    os.system(f'py manage.py createsuperuser --username={admin_name} --email=admin@example.com --noinput')

    print("Ремиграция успешно выполена")
    print(f"Суперпользователь создан с логином: {admin_name} и паролем: {admin_password}")

    os.system(f'py manage.py createsuperuser --username=user2 --email=admin@example.com --noinput')
    print(f"Суперпользователь user2 c паролем: {admin_password} создан")
    # print(f"Запускается сервер на проте: {port}")
    # print(f"Адрес админки: http://127.0.0.1:{port}/admin/")
    print('Запускается ws сервер')
    subprocess.Popen(["daphne", f"{project_name}.asgi:application", "-b", "0.0.0.0", "-p", str(int(port)+1)])

    print(f'ws сервер запущен на порте {str(int(port)+1)}')
    print(f'Запускается сервер Django на порте {port}')
    print(f"Адрес админки: http://127.0.0.1:{port}/admin/")

    subprocess.run(["py", "manage.py", "runserver", port])


if __name__ == '__main__':
    remigrate()
