import os
import subprocess
import asyncio
import time

from sys import argv

script, port = argv
port = int(port)
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
print(port)
def get_project_name():
    current_dir = os.path.abspath(os.getcwd())
    for dirpath, dirnames, filenames in os.walk(current_dir):
        if 'venv' in dirnames:
            dirnames.remove('venv')
        if 'settings.py' in filenames:
            return os.path.basename(dirpath)
    raise FileNotFoundError("Файл settings.py не найден в текущем каталоге или его родительских каталогах.")



# async def run_server(command):
#     process = await asyncio.create_subprocess_shell(command)
#     await process.communicate()

project_name = get_project_name()


print('Запускается ws сервер')
subprocess.Popen(["daphne", f"{project_name}.asgi:application", "-b", "0.0.0.0", "-p", f"{port + 1}"])
print(f'ws сервер запущен на порте {port + 1}')

print(f'Запускается сервер Django на порте {port}')
print(f"Адрес админки: http://127.0.0.1:{port}/admin/")
subprocess.run(["py", "manage.py", "runserver", f"{port}"])
print('Cервер Django запущен')



