##
# timer.py
#   Demo TIBRV Timer Callback
#
# LAST MODIFIED: V1.0 2016-12-22 ARIEN arien.chen@gmail.com
#
import sys
import time
from pytibrv.Tibrv import *
from datetime import datetime

class TimerApp(TibrvTimerCallback):

    def __init__(self, que: TibrvQueue, interval):
        self.tm = TibrvTimer()
        self.que = que

        status = self.tm.create(que, self, interval)
        assert TIBRV_OK == status, TibrvStatus.text(status)


    # Override TibrvTimerCallback.callback()
    def callback(self, event, msg, closure):
        print('HI', datetime.now())

    def run(self, sec):
        disp = TibrvDispatcher()
        status = disp.create(self.que)

        assert TIBRV_OK == status, TibrvStatus.text(status)

        timeout = time.time() + sec
        cnt = 0

        while time.time() <= timeout:
            cnt += 1
            print(cnt, 'WAITING ...')
            time.sleep(1.0)

        del disp

    def run2(self, sec):

        timeout = time.time() + sec
        cnt = 0

        while time.time() <= timeout:
            status = self.que.timedDispatch(1.0)
            cnt += 1
            print(cnt, 'WAITING ...')
            # no need to sleep, unless using TibrvQueue.poll()
            #time.sleep(1.0)


# MAIN PROGRAM
def main(argv):

    status = Tibrv.open()
    assert TIBRV_OK == status, TibrvStatus.text(status)

    # DEFAULT QUE
    que = TibrvQueue()

    # Timer for 0.5 sec
    tm = TimerApp(que, 0.5)

    # Run for 10 sec by TibrvQueue.timedDispatch()
    print('run2()')
    tm.run2(10.0)

    # Run for 10 sec by TibrvDispatcher
    print('run()')
    tm.run(10.0)


    Tibrv.close()
    print('TIBRV CLOSED')

if __name__ == "__main__":
    main(sys.argv)
