import os
import shutil


def mkfolder(path: str, name: str) -> None:
    """Создание папки в указанной директории.
    ~
    path — директория, в которой необходимо создать папку.
    name — наименование создаваемой папки. """
    os.mkdir(os.path.join(path, name))


def delfolder(path: str, del_folder: str) -> None:
    """Удаление указанной директории. Нельзя удалить не пустую папку (Необходим shutil.rmtree (?)...)
    ~
    path — директория, в которой необходимо удалить папку.
    name — наименование удаляемой папки."""
    os.rmdir(os.path.join(path, del_folder))


def showdirectory(path: str) -> None:
    """Печать содержимого директории.
    ~
    path — директория, содержимое которой необходимо напечатать.
    """
    content = os.listdir(path)
    print(*content, sep='\n')


def createfile(path: str, name: str) -> None:
    """Создание пустого файла в указанной директории.
    ~
    path — директория, в которой необходимо создать файл.
    name — наименование создаваемого файла."""
    with open(os.path.join(path, name), 'w'):
        pass


def delfile(path: str, name: str) -> None:
    """Создание пустого файла в указанной директории.
    ~
    path — директория, в которой необходимо удалить файл.
    name — наименование удаляемого файла."""
    os.remove(os.path.join(path, name))


def renamefile(path: str, name: str, new_name: str) -> None:
    """Переименование файла в указанной директории.
    ~
    path — директория, в которой необходимо переименовать файл.
    name — текущее наименование файла.
    new_name — новое наименование файла."""
    file = os.path.join(path, name)
    os.rename(file, os.path.join(path, new_name))


def movefile(path: str, name: str, new_path: str) -> None:
    """Перемещение файла из одной директории в другую.
    ~
    path — текущая директория файла, который необходимо переместить.
    name — наименование файла.
    new_path — новая директория файла.
    """
    os.rename(os.path.join(path, name), os.path.join(new_path, name))


def copyfile(path: str, name: str, new_path: str) -> None:
    shutil.copyfile(os.path.join(path, name), os.path.join(new_path, name))


def writetext(path: str, text: str, file: str) -> None:
    """Запись текстовой информации в файл в указанной директории.
    ~
    path — директория файла.
    text — текст, который запишется в файл.
    file — файл.
    """
    with open(os.path.join(path, file), 'w') as file:
        file.write(text)


def readtext(path: str, file: str) -> bytes:
    """Чтение файла в указанной директории.
    ~
    path — директория файла.
    file — файл, содержимое которого необходимо прочитать."""
    with open(os.path.join(path, file), 'rb') as file:
        return file.read()
