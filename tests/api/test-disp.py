import time
from pytibrv.disp import *
import unittest

class DispatcherTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = tibrv_Open()
        if status != TIBRV_OK:
            raise TibrvError(status)

    @classmethod
    def tearDownClass(cls):
        tibrv_Close()

    def test_create(self):

        que = TIBRV_DEFAULT_QUEUE

        status, disp = tibrvDispatcher_Create(que, 1.0)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvDispatcher_SetName(disp, 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, name = tibrvDispatcher_GetName(disp)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('TEST', name)

        status = tibrvDispatcher_Destroy(disp)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


if __name__ == "__main__" :
    unittest.main(verbosity=2)
