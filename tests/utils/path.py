from pulsar.apps.test import unittest
from pulsar.utils.path import Path

class TestPath(unittest.TestCase):
    
    def testThis(self):
        p = Path(__file__)
        self.assertTrue(p.isfile())
        self.assertFalse(p.isdir())
        c = Path.cwd()
        self.assertNotEqual(p,c)
        self.assertTrue(c.isdir())
        
    def testDir(self):
        c = Path.cwd()
        self.assertEqual(c,c.dir())
        c = Path('/sdjc/scdskjcdnsd/dhjdhjdjksdjksdksd')
        self.assertFalse(c.exists())
        self.assertRaises(ValueError, c.dir)
         
    def testAdd2Python(self):
        p = Path('/sdjc/scdskjcdnsd/dhjdhjdjksdjksdksd')
        module = p.add2python('pulsar')
        self.assertEqual(module, 'pulsar')
        self.assertRaises(ValueError, p.add2python, 'kaputttt')