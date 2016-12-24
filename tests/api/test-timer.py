from datetime import datetime
import time
from pytibrv.status import *
from pytibrv.api import *
from pytibrv.events import *
from pytibrv.disp import *
from pytibrv.queue import *
import unittest


def callback(event:tibrvEvent, message:tibrvMsg, closure):

    test = tibrvClosure(closure)
    test.counter += 1
    print(test.counter, datetime.now())
    if test.counter >= 10:
        status = tibrvEvent_Destroy(event)
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

        test.tm = 0

class TimerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = tibrv_Open()
        assert status == TIBRV_OK, tibrvStatus_GetText(status)

    @classmethod
    def tearDownClass(cls):
        tibrv_Close()


    def test_create(self):

        self.counter = 0

        status, que = tibrvQueue_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, disp = tibrvDispatcher_Create(que)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        print('')

        # pass self as closure
        # self.tm will assign to 0 when self.counter >= 0
        status, tm = tibrvEvent_CreateTimer(que, callback, 1.0, self)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        self.tm = tm

        # run for 11 seconds
        timeout = time.time() + 11

        while time.time() <= timeout:
            time.sleep(0.5)
            # wait till callback() destroy iteself when counter >= 10
            if self.tm == 0:
                break;
            #print('SLEEP...')

        # timer should be destroyed in callback()
        status = tibrvEvent_Destroy(tm)
        self.assertEqual(TIBRV_INVALID_EVENT, status, tibrvStatus_GetText(status))

        self.assertEqual(10, self.counter)

        status = tibrvQueue_Destroy(que)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        print('TEST DONE')

if __name__ == "__main__" :
    unittest.main(verbosity=2)
