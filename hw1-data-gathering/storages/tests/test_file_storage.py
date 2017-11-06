import os
import shutil
import unittest

from storages import file_storage


class TestFileStorage(unittest.TestCase):
    cache_prefix = 'test'

    def setUp(self):
        self.c = file_storage.FileStorage(self.cache_prefix)
        self.test_dir = self.c._directory_path

    def tearDown(self):
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_put(self):
        self.c._directory_path = self.test_dir
        res = self.c.put('f', 'test')
        self.assertTrue(res)
        self.assertEqual(1, len(os.listdir(self.test_dir)))

    def test_get(self):
        self.c._directory_path = self.test_dir
        self.c.put('f', 'test')

        c2 = file_storage.FileStorage(self.cache_prefix)
        c2._directory_path = self.test_dir
        val = c2.get('f')
        self.assertEqual('test', val)

    def test_has(self):
        self.c._directory_path = self.test_dir
        self.c.put('f', 'test')

        c2 = file_storage.FileStorage(self.cache_prefix)
        c2._directory_path = self.test_dir
        self.assertTrue(c2.has('f'))
        self.assertFalse(c2.has('f2'))

    def test_delete(self):
        self.c._directory_path = self.test_dir
        self.c.put('f', 'test')
        self.assertEqual(1, len(os.listdir(self.test_dir)))

        c2 = file_storage.FileStorage(self.cache_prefix)
        c2._directory_path = self.test_dir
        c2.delete('f')
        self.assertEqual(0, len(os.listdir(self.test_dir)))

    def test_flush(self):
        self.c._directory_path = self.test_dir
        self.c.put('f', 'test')
        self.c.put('f2', 'test2')
        self.assertEqual(2, len(os.listdir(self.test_dir)))
        self.assertTrue(os.path.isdir(self.test_dir))

        self.c.flush()
        self.assertFalse(os.path.isdir(self.test_dir))

    def test_keys(self):
        self.c._directory_path = self.test_dir
        self.c.put('f', 'test')
        self.c.put('f2', 'test2')
        self.c.put('f3', 'test3')
        self.assertEqual(['f', 'f2', 'f3'], self.c.keys())
        self.c.put('f4', 'test3')
        self.assertEqual(['f', 'f2', 'f3', 'f4'], self.c.keys())

        c2 = file_storage.FileStorage(self.cache_prefix)
        self.c.delete('f2')
        self.assertEqual(['f', 'f3', 'f4'], c2.keys())
