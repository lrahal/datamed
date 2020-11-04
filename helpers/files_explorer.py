import os
from typing import List, Dict


def listdir_nohidden(path: str):
    """
    List not hidden files in directory
    Avoid .DS_Store files for Mac
    """
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def write_txt_file(path: str, list_to_write: List):
    with open(path, 'w') as f:
        for item in list_to_write:
            f.write("%s\n" % item)


def write_csv(dict_to_write: Dict, path: str, fieldnames: List):
    with open(path, 'w', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(fieldnames)
        for key, value in dict_to_write.items():
            w.writerow([key, value])
