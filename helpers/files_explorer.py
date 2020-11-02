import os


def listdir_nohidden(path: str):
    """
    List not hidden files in directory
    Avoid .DS_Store files for Mac
    """
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f