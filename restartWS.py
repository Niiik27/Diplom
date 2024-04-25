import os
import subprocess
from sys import argv

script, port = argv
print(port)
def get_project_name():
    current_dir = os.path.abspath(os.getcwd())
    for dirpath, dirnames, filenames in os.walk(current_dir):
        if 'venv' in dirnames:
            dirnames.remove('venv')
        if 'settings.py' in filenames:
            return os.path.basename(dirpath)
    raise FileNotFoundError("Файл settings.py не найден в текущем каталоге или его родительских каталогах.")

project_name = get_project_name()
print('Запускается ws сервер')
subprocess.Popen(["daphne", f"{project_name}.asgi:application", "-b", "0.0.0.0", "-p", str(int(port) + 1)])
print(f'ws сервер запущен на порте {str(int(port) + 1)}')
print(f'Запускается сервер Django на порте {port}')
print(f"Адрес админки: http://127.0.0.1:{port}/admin/")
subprocess.run(["py", "manage.py", "runserver", port])
print('Cервер Django запущен')
