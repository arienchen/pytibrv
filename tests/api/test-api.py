from pytibrv.api import *
from pytibrv.status import *
import unittest

class VersionTest(unittest.TestCase):

    def setUp(self):
        status = tibrv_Open()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

    def tearDown(self):
        status = tibrv_Close()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

    def test_version(self):

        print('')
        ver = tibrv_Version()
        print('TIBRV VERSION:', ver)
        self.assertIsNotNone(ver)
        #self.assertEqual('8.4.5', ver)

if __name__ == "__main__":
    unittest.main(verbosity=2)
