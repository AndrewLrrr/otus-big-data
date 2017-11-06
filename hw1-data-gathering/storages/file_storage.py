import os
import errno
import shutil

from settings import STORAGE_PATH


class FileStorage:
    def __init__(self, prefix=''):
        if prefix and not prefix.startswith('/'):
            prefix = '/' + prefix
        self._directory_path = STORAGE_PATH + os.path.realpath(prefix)

    def put(self, key, value):
        try:
            os.makedirs(self._directory_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        file_path = os.path.join(self._directory_path, key)
        if os.path.isfile(file_path):
            return False
        with open(file_path, encoding='utf-8', mode='w') as fn:
            fn.write(value)
        return True

    def get(self, key):
        file_path = os.path.join(self._directory_path, key)
        if os.path.isfile(file_path):
            with open(file_path, encoding='utf-8', mode='r') as fn:
                res = fn.read()
            return res
        else:
            return None

    def has(self, key):
        file_path = os.path.join(self._directory_path, key)
        return os.path.isfile(file_path)

    def update(self, key, value):
        file_path = os.path.join(self._directory_path, key)
        if os.path.isfile(file_path):
            with open(file_path, encoding='utf-8', mode='w') as fn:
                fn.write(value)
            return True
        return False

    def delete(self, key):
        file_path = os.path.join(self._directory_path, key)
        try:
            os.remove(file_path)
            return True
        except OSError:
            return False

    def flush(self):
        try:
            shutil.rmtree(self._directory_path)
            return True
        except OSError:
            return False

    def keys(self):
        return os.listdir(self._directory_path)
