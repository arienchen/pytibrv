from datetime import datetime
import time
from pytibrv.Tibrv import *
import unittest

class TimerTest(unittest.TestCase, TibrvTimerCallback):

    @classmethod
    def setUpClass(cls):
        status = Tibrv.open()
        if status != TIBRV_OK:
            raise TibrvError(status)

    @classmethod
    def tearDownClass(cls):
        Tibrv.close()

    def callback(self, event: TibrvTimer, msg, closure):
        self.counter += 1
        print(self.counter, datetime.now())
        if self.counter >= 10:
            status = event.destroy()


    def test_create(self):

        self.counter = 0

        que = TibrvQueue()
        que.create('TIMER TEST')
        disp = TibrvDispatcher()
        status = disp.create(que)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        print('')

        tm = TibrvTimer()
        status = tm.create(que, self, 1.0)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        # run for 11 seconds
        self.timeout = time.time() + 11

        while time.time() <= self.timeout:
            time.sleep(0.5)
            # wait till callback() destroy iteself when counter >= 10
            if tm.id() == 0:
                break;
            #print('SLEEP...')

        status = disp.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        self.assertEqual(10, self.counter)

        # Timer had been destroyed in callback
        status = tm.destroy()
        self.assertEqual(TIBRV_INVALID_EVENT, status, TibrvStatus.text(status))

        status = que.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        print('TEST DONE')

if __name__ == "__main__" :
   unittest.main(verbosity=2)
