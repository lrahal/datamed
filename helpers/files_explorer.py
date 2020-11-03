import os
from typing import List


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
