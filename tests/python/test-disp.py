import time
from pytibrv.Tibrv import *
import unittest

class DispatcherTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = Tibrv.open()
        if status != TIBRV_OK:
            raise TibrvError(status)

    @classmethod
    def tearDownClass(cls):
        Tibrv.close()

    def test_create(self):

        # create default que
        que = TibrvQueue()
        disp = TibrvDispatcher()
        status = disp.create(que, 1.0)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        # default name is 'dispatcher'
        # self.assertEqual(None, disp.name)

        disp.name = 'TEST'
        self.assertEqual('TEST', disp.name)

        # dispatcher is a thread calling tibrvQueue_TimedDispach
        # nothing to test now
        del disp
        del que


if __name__ == "__main__" :
    unittest.main(verbosity=2)
