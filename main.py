"""
Лабораторная работа 1. Файловый менеджер
"""
__author__ = 'Sorokina Nadezda, ZB-PI21-2'

import platform
from config import MAIN_DIRECTORY
from functions import *
from pathlib import Path

current_directory = str(Path(MAIN_DIRECTORY))


if __name__ == '__main__':
    print(f"\033[34m\033[3m OS: \033[0m {platform.platform()} \n"
          f"\033[34m\033[3m Рабочая папка: \033[0m {MAIN_DIRECTORY}"
          f"\n В рамках данной программы нельзя выходить за пределы рабочей директории."
          f"Для смены рабочей директории измените конфигурационный файл. \n"
          f"Введите\033[33m 'help'\033[0m для вывода всех команд.\n")
    while True:
        print(f'\033[34m Текущая директория:\033[0m {current_directory} \n')
        user_input = input('\033[1m Введите команду:\033[0m ')
        if user_input == 'help':
            print("0. Печать содержимого текущей директории.\n"
                  "1. Создание папки в текущей директории.\n"
                  "2. Удаление папки в текущей директории.\n"
                  "3. Перейти в директорию.\n"
                  "4. Подняться на уровень выше.\n"
                  "5. Создание пустого файла в текущей директории.\n"
                  "6. Запись текста в файл.\n"
                  "7. Просмотр содержимого файла.\n"
                  "8. Удаление файла в текущей директории.\n"
                  "9. Копирование файла из одной папки в другую.\n"
                  "10. Перемещение файла из одной папки в другую.\n"
                  "11. Переименование файла в текущей директории.\n"
                  "exit. Выход из консольного приложения. \n")

        elif user_input == '0':
            showdirectory(current_directory)

        elif user_input == '1':
            new_folder = input("Введите название создаваемой папки: ")
            path = os.path.join(current_directory, new_folder)
            if os.path.exists(path):
                print("Папка с таким именем уже существует в данной директории.")
                continue
            mkfolder(current_directory, new_folder)
            print(f'Папка "{path}" создана.')

        elif user_input == '2':
            deleted_folder = input("Введите название удаляемой папки: ")
            path = os.path.join(current_directory, deleted_folder)
            if not os.path.exists(path):
                print("Папка с таким именем не существует в данной директории.")
                continue
            if not os.path.isdir(path):
                print("Это не папка, а файл.")
                continue
            if len(os.listdir(path)) != 0:
                print("Нельзя удалить не пустую папку.")
                continue
            delfolder(current_directory, deleted_folder)
            print(f'Папка "{path}" удалена.')

        elif user_input == '3':
            new_directory = input("Введите название директории, куда хотите перейти: ")
            path = os.path.join(current_directory, new_directory)
            if not os.path.exists(path):
                print("Путь не существует.")
                continue
            if not os.path.isdir(path):
                print("Нельзя перейти в файл.")
                continue
            current_directory = path

        elif user_input == '4':
            if not (current_directory == MAIN_DIRECTORY):
                current_directory = os.path.split(current_directory)[0]
            else:
                print("Невозможно выйти за пределы рабочей директории.")

        elif user_input == '5':
            file_name = input('Введите название файла: ')
            path = os.path.join(current_directory, file_name)
            if os.path.exists(path):
                print("Файл с таким именем уже существует в данной директории.")
                continue
            createfile(current_directory, file_name)
            print(f'Файл "{path}" успешно создан.')

        elif user_input == '6':
            text = input("Введите текст, который хотите записать в файл: ")
            file = input("Введите имя файла: ")
            path = os.path.join(current_directory, file)
            if not os.path.exists(path):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.isfile(path):
                print("Это не файл.")
                continue
            writetext(current_directory, text, file)
            print(f'Строка "{text}" успешно записана в файл {path}.')

        elif user_input == '7':
            file = input("Введите имя файла, содержимое которого необходимо прочитать: ")
            if not os.path.exists(os.path.join(current_directory, file)):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.isfile(os.path.join(current_directory, file)):
                print("Это не файл.")
                continue
            print(readtext(current_directory, file))

        elif user_input == '8':
            deleted_file = input("Введите имя удаляемого файла: ")
            path = os.path.join(current_directory, deleted_file)
            if not os.path.exists(path):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.isfile(path):
                print("Это не файл.")
                continue
            delfile(current_directory, deleted_file)
            print(f'Файл "{path}" успешно удален.')

        elif user_input == '9':
            file = input("Введите имя файла, который хотите скопировать: ")
            current_path = os.path.join(current_directory, file)
            if not os.path.exists(current_path):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.isfile(current_path):
                print("Это не файл.")
                continue

            new_file_directory = os.path.join(MAIN_DIRECTORY, path := Path(input(
                "Введите директорию, куда хотите копировать (относительно корня рабочей "
                "директории (" + MAIN_DIRECTORY + ") ")))
            if not os.path.exists(current_path):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.exists(new_file_directory):
                print("Папка с таким именем не существует в данной директории.")
                continue
            if os.path.exists(os.path.join(new_file_directory, file)):
                print("Файл с таким именем существует в директории, куда вы хотите скопировать файл.")
                continue
            copyfile(current_directory, file, new_file_directory)
            print(f'Файл "{file}" успешно скопирован в директорию {new_file_directory}.')

        elif user_input == '10':
            file = input("Введите имя файла, который хотите переместить: ")
            current_path = os.path.join(current_directory, file)
            if not os.path.exists(current_path):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.isfile(current_path):
                print("Это не файл.")
                continue

            new_file_directory = os.path.join(MAIN_DIRECTORY, path := Path(input(
                "Введите директорию, куда хотите переместить файл (относительно корня рабочей "
                "директории (" + MAIN_DIRECTORY + ") ")))
            if path.is_absolute():
                print("Пожалуйста, введите относительный путь.")
                continue
            if not os.path.exists(new_file_directory):
                print("Папка с таким именем не существует в данной директории.")
                continue
            if os.path.exists(os.path.join(new_file_directory, file)):
                print("Файл с таким именем существует в директории, куда вы хотите переместить файл.")
                continue
            movefile(current_directory, file, new_file_directory)
            print(f'Файл "{file}" успешно перемещен в директорию {new_file_directory}.')

        elif user_input == '11':
            file = input("Введите имя файла, который хотите переименовать: ")
            if not os.path.exists(os.path.join(current_directory, file)):
                print("Файл с таким именем не существует в данной директории.")
                continue
            if not os.path.isfile(os.path.join(current_directory, file)):
                print("Это не файл.")
                continue

            new_name = input("Введите новое имя файла: ")
            path = os.path.join(current_directory, new_name)
            if os.path.exists(os.path.join(current_directory, new_name)):
                print("Файл с таким именем уже существует в данной директории.")
                continue
            renamefile(current_directory, file, new_name)
            print(f'Файл "{file}" успешно переименован в {new_name}.')

        elif user_input == 'exit':
            print(f'До свидания. Счастья, здоровья.')
            break
        else:
            print("Неизвестная команда.")
