from pytibrv.api import Tibrv
from pytibrv.status import *
import unittest

class VersionTest(unittest.TestCase):

    def setUp(self):
        status = Tibrv.open()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

    def tearDown(self):
        status = Tibrv.close()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

    def test_version(self):

        print('')
        ver = Tibrv.version()
        print('TIBRV VERSION:', ver)
        self.assertIsNotNone(ver)
        #self.assertEqual('8.4.5', ver)

if __name__ == "__main__" :
   unittest.main(verbosity=2)
