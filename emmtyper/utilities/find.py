import os


def find(filename, path):
    for root, dirs, files in os.walk(os.path.dirname(path), topdown=True):
        for name in files:
            if name == filename:
                return os.path.join(root, name)
