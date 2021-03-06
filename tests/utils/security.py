import pulsar
from pulsar.apps.test import unittest
from pulsar.utils import security


class TestSecurity(unittest.TestCase):
    
    def testSalt(self):
        s1 = security.gen_salt(10)
        self.assertEqual(len(s1), 10)
        self.assertNotEqual(security.gen_salt(10), s1)
        s1 = security.gen_salt(30)
        self.assertEqual(len(s1), 30)
        self.assertRaises(ValueError, security.gen_salt, 0)
        
    def testPassword(self):
        password = 'my-test$$-password'
        hash = security.generate_password_hash(password)
        self.assertTrue('$' in hash)
        self.assertFalse(security.check_password_hash('bla', 'bla'))
        self.assertFalse(security.check_password_hash(hash, 'bla'))
        self.assertFalse(security.check_password_hash(hash, 'bla$foo'))
        self.assertTrue(security.check_password_hash(hash, password))