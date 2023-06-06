"""
Модуль вспомогательных функций.
"""
import os
from pathlib import Path
import csv


def get_full_size_directory(start_path='.') -> int:
    total_size = 0
    for dir_path, dir_names, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dir_path, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def get_full_path(base_folder, path: str) -> str | None:
    if path is None:
        return None
    if len(path) > 0 and (path[0] == "/" or path[0] == "\\"):
        path = path[1:]
    return os.path.join(Path(base_folder), Path(path))


def create_folder_if_not_exist(folder: str) -> None:
    folder = os.path.dirname(folder + "/")
    if folder is None or folder == '':
        return
    if not os.path.exists(folder):
        os.makedirs(folder)


def read_dic(filename: str) -> dict[str, str]:
    if not os.path.exists(filename):
        return dict()
    with open(filename, "r", newline='') as File:
        reader = csv.reader(File)
        d = dict()
        for row in reader:
            d[row[0]] = row[1]
        return d


def write_dic(filename: str, dic: dict[str, str]) -> None:
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for key in dic:
            writer.writerow([key, dic[key]])


