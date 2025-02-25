import unittest
from app.installation_test import install_check

class TestInstallCheck(unittest.TestCase):
    def test_install_dict(self):
        c=install_check()
        self.assertTrue(isinstance(c,dict))
