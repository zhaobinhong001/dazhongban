# coding:utf-8
"""
基本的自动化测试脚本 basic_demo.py
"""
__author__ = 'zheng'
 
import unittest
 
 
class TestStringMethods(unittest.TestCase):
 
    def setUp(self):
        print 'init by setUp...'
 
    def tearDown(self):
        print 'end by tearDown...'
 
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
 
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
        self.assertTrue('Foo'.isupper())
 
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
 
 
if __name__ == '__main__':
    unittest.main()