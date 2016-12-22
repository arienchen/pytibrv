import datetime
import time
from tibrv.tport import *
from tibrv.status import *
from tibrv.tport import *
from tibrv.events import *
from tibrv.disp import *
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

    def callback(self, event: TibrvTimer, closure):
        self.counter += 1
        print(self.counter, datetime.now())
        if self.counter >= 10:
            status = event.destroy()


    def test_create(self):

        self.counter = 0

        que = TibrvQueue()
        que.create('TIMER TEST')

        print('')

        tm = TibrvTimer()
        status = tm.create(que, self, 1.0)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        self.timeout = time.time() + 20000

        while time.time() <= self.timeout:
            time.sleep(0.6)
            if tm.id() == 0:
                break;
            #print('SLEEP...')

        self.assertEqual(10, self.counter)

        tm.destroy()

        del tm
        del que

        print('TEST DONE')

if __name__ == "__main__" :
   unittest.main(verbosity=2)
